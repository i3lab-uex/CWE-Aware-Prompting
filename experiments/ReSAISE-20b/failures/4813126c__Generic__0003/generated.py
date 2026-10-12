import re
from urllib.parse import urlparse, ParseResult

# List of approved domains (including subdomains)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "flickr.com",
    "images.example.org",   # replace with real trusted domains
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_subdomain(host: str, domain: str) -> bool:
    """
    Return True if `host` is the same as `domain` or a sub‑domain of it.
    """
    if host == domain:
        return True
    # Ensure host ends with ".domain" and is not something like "badimgur.com"
    return host.endswith("." + domain)


def verify_image_url(img_url: str) -> str:
    """
    Verify that an image URL belongs to a trusted domain.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is considered safe.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https or if the domain is not trusted.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    parsed: ParseResult = urlparse(img_url)

    # Validate scheme
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    hostname = parsed.hostname or ""
    if not any(_is_subdomain(hostname.lower(), d) for d in _TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain: {hostname}")

    # Re‑compose the URL to avoid trailing spaces or other subtle issues
    verified_url = parsed.geturl()
    return verified_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(verify_image_url("https://i.imgur.com/abcd1234.png"))
#     except ValueError as e:
#         print(e)