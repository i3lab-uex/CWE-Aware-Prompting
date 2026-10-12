import re
from urllib.parse import urlparse, urljoin

# Domains that are considered safe for external redirects (e.g. CDN, partner sites)
SAFE_DOMAINS = [
    "example.com",
    "cdn.example.org",
    "partner-site.net",
]

# Regular expression to match a hostname (IPv4, IPv6 or domain)
HOSTNAME_RE = re.compile(r"""
    ^(?:
        # IPv4
        (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|1?\d{1,2})
        |
        # IPv6
        \[[0-9a-fA-F:]+\]
        |
        # Domain name (allow subdomains)
        [a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+
    )$
""", re.VERBOSE | re.IGNORECASE)


def _is_valid_hostname(hostname: str) -> bool:
    """Return True if the hostname matches a valid IPv4/IPv6 or domain name."""
    return bool(HOSTNAME_RE.match(hostname))


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URI after successful login.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. https://app.example.com).
    next_path : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points outside the application domain or an allowed external domain.
    """
    # Parse primary base URL
    base = urlparse(primary_url)
    if not base.scheme or not base.netloc:
        raise ValueError("primary_url must be a valid absolute URL")

    # Resolve the next_path against the base
    resolved = urljoin(primary_url, next_path)

    # Parse the resolved URL to inspect its components
    parsed = urlparse(resolved)

    # If no scheme, treat as relative and return it
    if not parsed.scheme:
        return resolved

    # Validate scheme: only http/https allowed
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Unsupported URL scheme")

    # Validate hostname
    host = parsed.hostname or ""
    if not _is_valid_hostname(host):
        raise ValueError("Malformed hostname in redirect URL")

    # Determine if the host is within the application domain
    primary_host = base.hostname.lower()
    target_host = host.lower()

    # Allow if same domain or subdomain
    if target_host == primary_host or target_host.endswith("." + primary_host):
        return resolved

    # Allow if host is in SAFE_DOMAINS
    if target_host in (d.lower() for d in SAFE_DOMAINS):
        return resolved

    raise ValueError("Redirect URL points to an untrusted domain")