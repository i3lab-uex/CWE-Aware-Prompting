import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Configuration:  Allowed external domains and subdomains.
# --------------------------------------------------------------------------- #
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.internal.net",
    # Add other approved domains here
}

# --------------------------------------------------------------------------- #
# Helper: Validate that hostname is not a private/reserved IP address.
# --------------------------------------------------------------------------- #
def _is_public_ip(hostname: str) -> bool:
    """
    Return True if the hostname resolves to a public IP address or is
    not an IP literal.  Non‑IP hostnames are considered safe at this step.
    """
    try:
        # If hostname is an IP literal, check its network class
        ip = ipaddress.ip_address(hostname)
        return not (ip.is_private or ip.is_loopback or
                    ip.is_reserved or ip.is_multicast or ip.is_link_local)
    except ValueError:
        # Not an IP literal – assume DNS will resolve to a public address
        return True

# --------------------------------------------------------------------------- #
# Main function: enforce_api_security
# --------------------------------------------------------------------------- #
def enforce_api_security(api_endpoint: str) -> str:
    """
    Validate that the supplied URL points to an approved external API endpoint.
    
    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unapproved domain,
        resolves to a private IP address, or uses an insecure scheme.
    """
    if not isinstance(api_endpoint, str):
        raise ValueError("api_endpoint must be a string")

    # Parse the URL
    parsed = urlparse(api_endpoint)
    
    # 1. Scheme must be https (or optionally http if explicitly allowed)
    if parsed.scheme.lower() != "https":
        raise ValueError("Only HTTPS URLs are allowed for external API calls")

    # 2. Hostname must be present
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # 3. Reject IP literals that are private or reserved
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname) or \
       re.match(r"^[0-9a-fA-F:]+$", hostname):
        if not _is_public_ip(hostname):
            raise ValueError(f"Private or reserved IP address detected: {hostname}")

    # 4. Check against approved domains
    # Allow subdomains of approved domains by matching suffix
    def is_allowed(host: str) -> bool:
        host = host.lower()
        for domain in ALLOWED_DOMAINS:
            if host == domain or host.endswith("." + domain):
                return True
        return False

    if not is_allowed(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved")

    # 5. Reconstruct the URL to ensure no unwanted fragments/parameters
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params
        parsed.query or "",  # allow query but could be filtered further
        ""   # fragment removed
    ))

    return safe_url

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         url = enforce_api_security("https://api.example.com/v1/resource?param=value")
#         print(f"Verified URL: {url}")
#     except ValueError as e:
#         print(f"Security check failed: {e}")