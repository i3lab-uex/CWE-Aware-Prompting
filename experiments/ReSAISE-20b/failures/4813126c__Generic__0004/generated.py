import re
from urllib.parse import urlparse

# A small set of trusted image hosting domains.
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "i.redd.it",
    "pbs.twimg.com",
    "media.discordapp.net",
    "cdn.discordapp.com",
    "flickr.com",
    "i.redditmedia.com",
    "cdn.akamai.steamstatic.com",
}

# Regular expression to validate URLs quickly (scheme + netloc).
_URL_RE = re.compile(r"^(https?://)[^\s/$.?#].[^\s]*$")


def verify_image_url(img_url: str) -> str:
    """
    Verify that the provided image URL points to a trusted domain.

    Parameters
    ----------
    img_url : str
        The image URL to be verified.

    Returns
    -------
    str
        The original image URL if it is considered safe and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not http/https, or if the host does not belong to a
        trusted domain.
    """
    # Quick sanity check for scheme and basic URL structure.
    if not _URL_RE.match(img_url):
        raise ValueError("Unrecognized or malformed URL")

    parsed = urlparse(img_url)
    scheme, netloc = parsed.scheme.lower(), parsed.netloc.lower()

    if scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {scheme}")

    # Strip port if present (e.g., example.com:443)
    host = netloc.split(":")[0]

    # Allow subdomains that end with a trusted domain.
    if not any(host == d or host.endswith("." + d) for d in _TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not in the list of trusted hosts")

    return img_url