import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: a whitelist of trusted RSS providers.
# Each entry may be a full domain (e.g. "rss.nytimes.com") or a pattern that
# accepts subdomains (e.g. r"^.*\.feedwordpress\.com$").
# --------------------------------------------------------------------------- #
WHITELIST = [
    r"^rss\.nytimes\.com$",
    r"^feeds\.google\.com$",
    r"^rss\.guardian\.co\.uk$",
    r"^feeds\.wordpress\.com$",
    r"^.*\.blogspot\.com$",      # allow any blogspot subdomain
    r"^feeds\.medium\.com$",
]

# --------------------------------------------------------------------------- #
# Private / internal IP ranges (RFC 1918, loopback, link-local).
# We reject any URL that resolves to these addresses.
# --------------------------------------------------------------------------- #
PRIVATE_IP_REGEX = re.compile(
    r"""
    (^127\.0\.0\.1$)|                                 # loopback
    (^10\.)|                                            # 10.0.0.0/8
    (^172\.1[6-9]\.)|                                  # 172.16.0.0/12
    (^172\.2[0-9]\.)|
    (^172\.3[0-1]\.)|
    (^192\.168\.)|                                     # 192.168.0.0/16
    (^169\.254\.)|                                     # link-local
    (^::1$)|                                           # IPv6 loopback
    (^fe80:|^fc00:|^fd00:)                               # IPv6 link-local / unique local
    """,
    re.VERBOSE,
)

# --------------------------------------------------------------------------- #
def _is_private_netloc(netloc: str) -> bool:
    """
    Determine whether a netloc is an IP address that falls into private
    or loopback ranges.  The function does not perform DNS resolution;
    it only checks literal IPs or IPv6 literals.
    """
    # Strip port if present
    host = netloc.split(":")[0]
    return PRIVATE_IP_REGEX.match(host) is not None

def _is_whitelisted(domain: str) -> bool:
    """
    Check if the given domain matches any of the whitelisted patterns.
    """
    for pattern in WHITELIST:
        if re.match(pattern, domain, re.IGNORECASE):
            return True
    return False

def check_rss_address(rss_address: str) -> str:
    """
    Validate an RSS feed URL and return a sanitized version that
    guarantees the URL points to a trusted provider.

    Parameters
    ----------
    rss_address : str
        The raw URL supplied by the caller.

    Returns
    -------
    str
        A normalized, safe URL that is guaranteed to point to an approved
        provider.

    Raises
    ------
    ValueError
        If the URL is malformed, points to an unapproved provider,
        or attempts to access a private/internal network.
    """
    if not rss_address:
        raise ValueError("RSS address must be a non-empty string")

    # Parse the URL
    parsed = urlparse(rss_address)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http/https allowed")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Reject URLs that point to private IPs or localhost
    if _is_private_netloc(parsed.netloc):
        raise ValueError("URL points to a private or internal network address")

    # Domain normalization: lower‑case and strip trailing dots
    domain = parsed.netloc.lower().rstrip(".")

    if not _is_whitelisted(domain):
        raise ValueError(f"Domain '{domain}' is not in the whitelist of trusted providers")

    # Re‑assemble a sanitized URL
    safe_parsed = parsed._replace(path=parsed.path or "/", params="", query="", fragment="")
    sanitized_url = urlunparse(safe_parsed)

    return sanitized_url