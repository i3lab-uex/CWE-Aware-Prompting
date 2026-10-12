import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "flickr.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "i.redd.it",
}

# Regular expression to validate a well‑formed URL
_URL_RE = re.compile(
    r"^(?P<scheme>https?)://"
    r"(?P<host>[^/:?#]+)"
    r"(?:[:](?P<port>\d+))?"
    r"(?P<path>/[^\s?#]*)?"
    r"(?:\?(?P<query>[^#]*))?"
    r"(?:#(?P<fragment>.*))?$",
    re.IGNORECASE,
)

def resolve_image_url(image_url: str) -> str:
    """
    Return the resolved image URL if its domain is trusted.
    
    Parameters
    ----------
    image_url : str
        The URL to be validated.

    Returns
    -------
    str
        The original URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or is malformed.
    """
    if not isinstance(image_url, str):
        raise ValueError("image_url must be a string")

    # Quick regex check for well‑formedness
    match = _URL_RE.match(image_url)
    if not match:
        raise ValueError("Malformed URL")

    # Parse the URL to extract components
    parsed = urlparse(image_url)
    
    host = parsed.hostname or ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalize the host to lowercase for comparison
    host_lower = host.lower()

    # Check if the host is in the trusted list (including subdomains)
    def is_trusted(hostname: str) -> bool:
        for domain in _TRUSTED_DOMAINS:
            # Allow subdomains of the trusted domain
            if hostname == domain or hostname.endswith("." + domain):
                return True
        return False

    if not is_trusted(host_lower):
        raise ValueError(f"Domain '{host}' is not trusted")

    # Re‑construct the URL to ensure it is canonical
    safe_url = urlunparse(parsed._replace(scheme="https"))
    return safe_url

# Example usage (commented out to avoid accidental execution)
# if __name__ == "__main__":
#     try:
#         print(resolve_image_url("https://i.imgur.com/example.png"))
#     except ValueError as e:
#         print(e)