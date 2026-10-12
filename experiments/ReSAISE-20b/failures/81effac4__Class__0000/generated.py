import re
import socket
from urllib.parse import urlparse, unquote
import ipaddress

# --------------------------------------------------------------------------- #
# Trusted domain list – extend this with your own domains or sub‑domains
# --------------------------------------------------------------------------- #
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.net",
    # Add more domains or use regex patterns if needed
}

# --------------------------------------------------------------------------- #
# Regular expression for detecting disallowed hostnames (e.g. localhost)
# --------------------------------------------------------------------------- #
LOCALHOST_RE = re.compile(r"^(localhost|127\.0\.0\.1)$", re.IGNORECASE)

# --------------------------------------------------------------------------- #
def check_api_link(api_link: str) -> str:
    """
    Validate that the supplied URL points to an externally reachable,
    trusted API endpoint.

    Parameters
    ----------
    api_link : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it passes all checks.

    Raises
    ------
    ValueError
        If the URL does not use http/https, points to an untrusted domain,
        or resolves to a private/internal IP address.
    """
    # 1. Basic parsing
    parsed = urlparse(api_link)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # 2. Normalize host (remove port, decode percent‑encoding)
    host = parsed.hostname
    if not host:
        raise ValueError("Hostname could not be extracted")

    # 3. Disallow localhost / loopback
    if LOCALHOST_RE.match(host):
        raise ValueError("Disallowed hostname: localhost or 127.0.0.1")

    # 4. Check against trusted domain list
    if not any(host == td or host.endswith("." + td) for td in TRUSTED_DOMAINS):
        raise ValueError(f"Hostname '{host}' is not in the trusted domain list")

    # 5. Resolve hostname to IP addresses
    try:
        addrinfo = socket.getaddrinfo(host, None, family=socket.AF_UNSPEC,
                                      type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for '{host}': {exc}") from exc

    # 6. Ensure all resolved IPs are public
    for family, _, _, _, sockaddr in addrinfo:
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue  # skip malformed entries

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local \
           or ip_obj.is_reserved or ip_obj.is_multicast:
            raise ValueError(
                f"Resolved IP {ip_str} for hostname '{host}' is not publicly routable"
            )

    # 7. Return the sanitized URL (re‑build to ensure consistent format)
    sanitized = parsed._replace(
        netloc=f"{host}:{parsed.port}" if parsed.port else host,
        path=unquote(parsed.path),
    ).geturl()

    return sanitized

# --------------------------------------------------------------------------- #
# Example usage
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data",
        "http://localhost/api",                 # should fail
        "https://192.168.1.10/resource",         # should fail
        "https://service.trusted.net:8080/endpoint",
    ]

    for url in test_urls:
        try:
            valid = check_api_link(url)
            print(f"[OK]   {valid}")
        except ValueError as e:
            print(f"[FAIL] {url} -> {e}")