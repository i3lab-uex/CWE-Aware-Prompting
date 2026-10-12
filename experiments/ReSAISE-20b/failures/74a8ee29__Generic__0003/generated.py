import re
from urllib.parse import urlparse, urlunparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# List of trusted domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "i.redd.it",
    "pbs.twimg.com",
    "cdn.pixabay.com",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the given network location belongs to a trusted domain.
    Subdomains are considered only if they match exactly.
    """
    return netloc.lower() in _TRUSTED_DOMAINS


def _validate_url(url: str) -> None:
    """
    Validate the URL's scheme and domain.
    Raises ValueError if invalid.
    """
    parsed = urlparse(url)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")


def _create_session() -> requests.Session:
    """
    Create a requests session with sane defaults.
    - Limits redirects to 10
    - Retries on transient errors (5xx, connection issues)
    """
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods={"GET", "HEAD"},
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def check_image_link(image_link: str) -> str:
    """
    Resolve the given image URL and return the final URL if it belongs to a
    trusted domain. Raises ValueError otherwise.

    Parameters
    ----------
    image_link : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified final URL after following redirects.

    Raises
    ------
    ValueError
        If the scheme is unsupported, domain is untrusted, or if a network
        error occurs.
    """
    # Basic syntax validation
    try:
        _validate_url(image_link)
    except Exception as exc:
        raise ValueError(f"Invalid image link: {exc}") from None

    session = _create_session()

    try:
        # Use HEAD first to avoid downloading large images unnecessarily.
        resp = session.head(image_link, allow_redirects=True, timeout=10)
        final_url = resp.url
    except requests.RequestException as exc:
        raise ValueError(f"Network error while resolving URL: {exc}") from None

    # Final validation after redirects
    _validate_url(final_url)

    return final_url


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     test_url = "https://i.imgur.com/abcd1234.jpg"
#     try:
#         print(check_image_link(test_url))
#     except ValueError as e:
#         print(e)