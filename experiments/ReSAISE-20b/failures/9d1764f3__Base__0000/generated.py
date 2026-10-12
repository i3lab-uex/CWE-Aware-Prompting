import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# --------------------------------------------------------------------------- #
# Whitelisted domains that are allowed to be used in internal API calls.
WHITELISTED_DOMAINS = {
    "api.example.com",
    "webhooks.service.org",
    "secure-connector.internal.company.net",
}

# --------------------------------------------------------------------------- #
def _is_ip_private(ip: str) -> bool:
    """
    Return True if the IP address is in a private, loopback,
    link-local, or reserved range that should not be reachable
    from the public internet.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        # Not a valid IP address
        return False

    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
    )


def _resolve_and_validate_domain(domain: str) -> None:
    """
    Resolve the domain name to IP addresses and ensure none of them
    are private or otherwise disallowed.
    """
    try:
        # getaddrinfo returns a list of (family, type, proto, canonname, sockaddr)
        results = socket.getaddrinfo(domain, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Domain resolution failed for '{domain}': {exc}") from exc

    for _, _, _, _, sockaddr in results:
        ip = sockaddr[0]
        if _is_ip_private(ip):
            raise ValueError(f"Domain '{domain}' resolves to private IP {ip}.")


def validate_webhook(webhook_link: str) -> str:
    """
    Validate an external webhook URL and return a secure, internal
    API URL that can be safely used by the server.

    Parameters
    ----------
    webhook_link : str
        The external URL supplied by an upstream component.

    Returns
    -------
    str
        A sanitized, validated URL that points to an approved domain.

    Raises
    ------
    ValueError
        If the URL's domain is not in the whitelist, or if it resolves to a
        private/internal IP address.
    """
    # Basic sanity check – ensure we have an absolute URL
    parsed = urlparse(webhook_link)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid URL format; expected absolute URL with scheme and host.")

    # Normalize the domain (lowercase, strip port)
    domain = parsed.hostname.lower()
    if not domain:
        raise ValueError("URL does not contain a valid hostname.")

    # Ensure the host is in our whitelist
    if domain not in WHITELISTED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not in the approved whitelist.")

    # Resolve DNS and check for private IPs
    _resolve_and_validate_domain(domain)

    # Reconstruct the URL to ensure we don't carry over any unsafe fragments
    safe_parts = (
        parsed.scheme,
        parsed.netloc,          # keep original netloc (hostname[:port])
        parsed.path or "",      # use empty string if path is None
        "",                     # query stripped for safety
        "",                     # fragment stripped for safety
    )
    safe_url = urlunparse(safe_parts)

    return safe_url


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/webhook?token=abc",
        "http://malicious.internal/endpoint",
        "https://unknown.com/path",
    ]

    for url in test_urls:
        try:
            print(f"Validated: {validate_webhook(url)}")
        except ValueError as e:
            print(f"Rejected: {e}")