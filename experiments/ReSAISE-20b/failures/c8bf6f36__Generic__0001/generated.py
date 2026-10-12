import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted RSS providers.  Add or remove domains as needed for your environment.
# The list should contain only fully qualified domain names, without scheme or
# trailing slashes.  Sub‑domains are matched explicitly.
TRUSTED_PROVIDERS = {
    "rss.nytimes.com",
    "feeds.feedburner.com",
    "blog.google/rss",
    "news.ycombinator.com",
    "rss.cnn.com",
    "feeds.bbci.co.uk",
    "news.google.com",
}

# Regular expression for detecting private / local IP ranges.
PRIVATE_IP_RE = re.compile(
    r"""
    ^(                                   # start of string
        10\.                               #   10.0.0.0 – 10.255.255.255
      | 172\.(1[6-9]|2\d|3[0-1])\.          #   172.16.0.0 – 172.31.255.255
      | 192\.168\.                          #   192.168.0.0 – 192.168.255.255
      | 127\.                                 #   Loopback (127.x.x.x)
    )
    """,
    re.VERBOSE,
)

def _is_private_netloc(netloc: str) -> bool:
    """
    Return True if the netloc contains a private IP address or localhost.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    # Detect IPv4 addresses directly (no DNS resolution)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        return bool(PRIVATE_IP_RE.match(host))
    # If it's a hostname, assume it resolves to an external address
    return False

def validate_rss_link(rss_link: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers.

    Parameters
    ----------
    rss_link : str
        The URL of the RSS feed being validated.

    Returns
    -------
    str
        A sanitized, normalized URL that is guaranteed to point to a trusted
        provider.

    Raises
    ------
    ValueError
        If the URL is not from an approved provider, uses an insecure scheme,
        or attempts to access a restricted internal network.
    """
    if not rss_link:
        raise ValueError("RSS link must be a non-empty string")

    parsed = urlparse(rss_link)

    # 1. Scheme must be https (or http for legacy but warn)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme '{parsed.scheme}'. Only http/https are allowed.")

    # 2. Ensure netloc is not a private IP or localhost
    if _is_private_netloc(parsed.netloc):
        raise ValueError("URL points to a private or local network address")

    # 3. Verify domain against trusted providers
    host = parsed.netloc.lower()
    # Strip port for comparison
    host_no_port = host.split(":")[0]
    if host_no_port not in TRUSTED_PROVIDERS:
        raise ValueError(f"Domain '{host_no_port}' is not an approved RSS provider")

    # 4. Reconstruct a clean URL (strip fragment, keep query)
    sanitized = urlunparse((
        parsed.scheme,
        host_no_port,
        parsed.path or "/",
        "",          # params
        parsed.query,  # keep query if present (e.g., pagination)
        "",          # fragment removed
    ))
    return sanitized

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# try:
#     url = validate_rss_link("https://feeds.feedburner.com/TechCrunch")
#     print("Valid URL:", url)
# except ValueError as e:
#     print("Invalid RSS link:", e)