import re
from urllib.parse import urlparse, urlunparse

# Approved domains for redirection – add any additional safe domains here
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Regular expression to match valid hostnames (IPv4, IPv6 or punycode)
HOSTNAME_RE = re.compile(
    r"^(?:"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+"  # subdomains
    r"[a-zA-Z]{2,63}"                                          # TLD
    r"|"
    r"\[([0-9a-fA-F:]+)\]"                                     # IPv6
    r"|"
    r"\d{1,3}(?:\.\d{1,3}){3}"                                 # IPv4
    r")$"
)

def _normalize_domain(host: str) -> str:
    """
    Normalise the domain part of a URL.
    - Lowercase
    - Strip leading 'www.'
    - Convert punycode to Unicode for comparison
    """
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    # Convert punycode (idna) to Unicode
    try:
        host = host.encode("ascii").decode("idna")
    except Exception:
        pass  # leave unchanged if not punycode
    return host

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user-supplied URL and return it only if its domain is approved.
    
    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        The original URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme, or its domain is not approved.
    """
    if not redirect_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Only allow http, https or relative paths (no other schemes)
    if parsed.scheme not in ("http", "https", ""):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # For relative URLs, just return them – they are inherently safe
    if parsed.netloc == "":
        # Ensure the path is not a full absolute URL disguised as a path
        if parsed.path.startswith("//"):
            raise ValueError("Path looks like an absolute URL")
        return urlunparse(parsed)

    # Validate host
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    # Ensure the host matches our regex
    if not HOSTNAME_RE.match(parsed.hostname):
        raise ValueError(f"Invalid hostname: {parsed.hostname}")

    # Normalize domain for comparison
    norm_domain = _normalize_domain(parsed.hostname)

    if norm_domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{norm_domain}' is not approved for redirection")

    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(parsed._replace(netloc=parsed.netloc.lower()))
    return safe_url