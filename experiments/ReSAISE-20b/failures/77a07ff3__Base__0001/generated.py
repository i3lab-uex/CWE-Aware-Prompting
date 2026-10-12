import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (example). Add your own.
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "api.safe-domain.net",
}

# Regex to detect IP addresses (IPv4 and IPv6)
IPV4_RE = re.compile(r"""
    ^
    (?:
      (?:25[0-5]|2[0-4]\d|1?\d{1,2})\.
    ){3}
    (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    $
""", re.VERBOSE)

IPV6_RE = re.compile(r"""
    ^
    \[
        (?:
            [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}
            |
            (?:[0-9a-fA-F]{1,4}:){1,7}:
            |
            (?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}
            |
            (?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}
            |
            (?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}
            |
            (?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}
            |
            (?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}
            |
            [0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}
            |
            :(?::[0-9a-fA-F]{1,4}){1,7}
            |
            ::
        )
    \]
    $
""", re.VERBOSE)


def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IPv4 or IPv6 address."""
    return IPV4_RE.match(host) is not None or IPV6_RE.match(host) is not None


def _normalize_domain(domain: str) -> str:
    """Normalize the domain for comparison."""
    # IDNA encoding handles internationalized domains
    return domain.lower().encode("idna").decode("ascii")


def process_url_redirect(input_url: str) -> str:
    """
    Validate and return a safe-to-use URL for redirection.

    Parameters
    ----------
    input_url : str
        The user-provided URL to be validated.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        or its domain is not in the approved list.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(input_url)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject raw IP addresses
    if _is_ip_address(host):
        raise ValueError("IP addresses are not allowed")

    # Normalize and check domain
    norm_domain = _normalize_domain(host)
    if norm_domain not in {_normalize_domain(d) for d in APPROVED_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not approved")

    # Reconstruct the URL to ensure no fragments or query tricks
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,  # includes host and optional port
        parsed.path or "",
        "",  # params
        parsed.query,  # keep query if needed; can be sanitized further
        "",  # fragment removed
    ))

    return safe_url