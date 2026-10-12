import re
from urllib.parse import urlparse, ParseResult

# List of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "imgur.com",
    "flickr.com",
    "tinypic.com",
    "postimages.org",
    "imgbb.com",
    "pbs.twimg.com",  # Twitter image host
    "i.redd.it",      # Reddit image host
}

# Regular expression to match a valid HTTP/HTTPS URL.
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<netloc>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE,
)

def _normalize_netloc(netloc: str) -> str:
    """
    Strip user info and port from a netloc.
    Example: 'user:pass@host.com:8080' -> 'host.com'
    """
    # Remove any userinfo (username:password@)
    if '@' in netloc:
        netloc = netloc.split('@', 1)[-1]
    # Remove port
    if ':' in netloc:
        netloc = netloc.split(':', 1)[0]
    return netloc.lower()

def _is_trusted_domain(netloc: str) -> bool:
    """
    Determine if the given netloc is within the list of trusted domains.
    Handles subdomains correctly.
    """
    for domain in TRUSTED_DOMAINS:
        # Exact match
        if netloc == domain:
            return True
        # Subdomain check: netloc ends with '.' + domain
        if netloc.endswith("." + domain):
            return True
    return False

def verify_image_url(img_url: str) -> str:
    """
    Verify that the provided image URL belongs to a trusted domain and
    uses an allowed scheme (http or https). If valid, return the URL.
    Raises ValueError otherwise.

    Parameters
    ----------
    img_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified image URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is untrusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Basic format validation
    match = URL_REGEX.match(img_url.strip())
    if not match:
        raise ValueError("Invalid URL format")

    scheme = match.group('scheme').lower()
    netloc_raw = match.group('netloc')
    path = match.group('path') or ""

    # Scheme check
    if scheme not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    # Normalize netloc (remove userinfo, port)
    netloc = _normalize_netloc(netloc_raw)

    # Domain trust check
    if not _is_trusted_domain(netloc):
        raise ValueError(f"Domain '{netloc}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    verified = f"{scheme}://{netloc}{path}"
    return verified

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         print(verify_image_url("https://i.imgur.com/abcd1234.png"))
#     except ValueError as e:
#         print(f"Verification failed: {e}")