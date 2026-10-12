import re
from urllib.parse import urlparse, urlunparse

# Regular expression to detect RFC1918 private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3})|"
    r"(172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3})|"
    r"(192\.168\.\d{1,3}\.\d{1,3})"
    r")$",
    re.IGNORECASE,
)

# List of approved domains (case‑insensitive).  Adjust as needed.
APPROVED_DOMAINS = {
    "api.example.com",
    "services.anotherdomain.org",
}

# Helper to determine if a hostname is an IP address
def _is_ip(hostname: str) -> bool:
    try:
        parts = hostname.split(".")
        if len(parts) != 4:
            return False
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP is in a private RFC1918 range."""
    return PRIVATE_IP_REGEX.match(ip) is not None


def check_api_endpoint(endpoint_url: str) -> str:
    """
    Validate that `endpoint_url` points to an approved external API endpoint.

    Raises:
        ValueError: If the URL is malformed, points to a private network,
                    or uses an unapproved domain.
    Returns:
        str: The validated, normalized URL (scheme + netloc + path).
    """
    if not endpoint_url:
        raise ValueError("Endpoint URL cannot be empty")

    # Parse the URL
    parsed = urlparse(endpoint_url)

    # Basic scheme check – only http/https are allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (hostname) is present
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Reject localhost or 127.0.0.1
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        raise ValueError("Localhost addresses are not allowed")

    # Reject any private IP address
    if _is_ip(parsed.hostname) and _is_private_ip(parsed.hostname):
        raise ValueError("Private IP addresses are not allowed")

    # Normalize hostname to lowercase for domain comparison
    host_lower = parsed.hostname.lower()

    # If the hostname is an IP, we must allow it only if it's explicitly whitelisted
    if _is_ip(host_lower):
        # Convert IP string to canonical form and compare against whitelist
        if host_lower not in APPROVED_DOMAINS:
            raise ValueError(f"IP address {host_lower} is not in the approved list")
    else:
        # Domain name – check against whitelist
        if host_lower not in APPROVED_DOMAINS:
            raise ValueError(f"Domain {host_lower} is not approved")

    # Reconstruct a clean URL (strip fragments, params)
    cleaned = parsed._replace(fragment="", query="")
    return urlunparse(cleaned)

# Example usage:
if __name__ == "__main__":
    try:
        url = check_api_endpoint("https://api.example.com/v1/resource?foo=bar#section")
        print(f"Verified URL: {url}")
    except ValueError as exc:
        print(f"Invalid endpoint: {exc}")