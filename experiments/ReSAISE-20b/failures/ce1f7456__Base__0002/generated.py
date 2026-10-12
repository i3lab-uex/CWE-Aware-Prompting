import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",  # internal domain
}

# Regular expression to detect IP addresses (IPv4 & IPv6)
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}
                |
                (?:[0-9a-fA-F]{1,4}:){1,7}:
                |
                (?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}
                |
                (?:[0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}
                |
                (?:[0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}
                |
                (?:[0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}
                |
                (?:[0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}
                |
                [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})
                |
                :((:[0-9a-fA-F]{1,4}){1,7}|:)
                |
                fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+
                |
                ::(ffff(:0{1,4}){0,1}:){0,1}
                ((25[0-5]|(2[0-4]|1{0,1}\d|)[0-9])\.){3}
                (25[0-5]|(2[0-4]|1{0,1}\d|)[0-9])
                |
                (?:[0-9a-fA-F]{1,4}:){1,4}:
                ((25[0-5]|(2[0-4]|1{0,1}\d|)[0-9])\.){3}
                (25[0-5]|(2[0-4]|1{0,1}\d|)[0-9])
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if host is a literal IP address."""
    return bool(_IP_REGEX.match(host))

def _normalize_domain(domain: str) -> str:
    """Normalize domain for comparison (case‑insensitive, punycode)."""
    # Convert Unicode to ASCII using IDNA
    try:
        return domain.encode("idna").decode("ascii").lower()
    except Exception:
        # Fallback: just lower case
        return domain.lower()

def secure_url_redirect(destination_url: str) -> str:
    """
    Sanitize a user‑provided URL for safe redirection.

    Parameters
    ----------
    destination_url : str
        The URL supplied by the user to redirect to.

    Returns
    -------
    str
        A sanitized, fully qualified URL that is guaranteed to point to an
        allowed domain.

    Raises
    ------
    ValueError
        If the destination URL does not resolve to an allowed domain,
        or if it is malformed.
    """
    # Parse the URL
    parsed = urlparse(destination_url)

    if not parsed.scheme or not parsed.netloc:
        # Treat relative URLs as safe only if they are purely path
        if not parsed.path or parsed.netloc:
            raise ValueError("Invalid URL: missing scheme or netloc.")
        # Allow relative path (e.g., "/home")
        return urlunparse(parsed)

    host = parsed.hostname
    if not host:
        raise ValueError("URL does not contain a hostname.")

    # Reject URLs that resolve to literal IP addresses
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed for redirection.")

    normalized_host = _normalize_domain(host)

    # Check if the host ends with any allowed domain
    if not any(
        normalized_host == d or normalized_host.endswith("." + d)
        for d in (ALLOWED_DOMAINS | {_normalize_domain(d) for d in ALLOWED_DOMAINS})
    ):
        raise ValueError(f"Domain '{host}' is not in the list of allowed domains.")

    # Reconstruct a clean URL (strip query params that might be malicious)
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",  # params
        "",  # query
        ""   # fragment
    )
    return urlunparse(safe_parts)

# Example usage:
if __name__ == "__main__":
    try:
        print(secure_url_redirect("https://example.com/login?token=abc"))
        print(secure_url_redirect("/dashboard"))  # relative path
    except ValueError as e:
        print(f"Redirection blocked: {e}")