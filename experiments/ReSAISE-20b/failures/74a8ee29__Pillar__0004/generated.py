import re
from urllib.parse import urlparse

import requests


# List of domains that are considered trusted for image hosting.
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    # Add more trusted domains here as needed.
}


def _is_trusted_domain(host: str) -> bool:
    """
    Check if the given host belongs to one of the trusted domains.
    Subdomains are accepted only if they match exactly an entry in
    _TRUSTED_DOMAINS.
    """
    # Normalize host: strip trailing dot, lower case
    host = host.lower().rstrip(".")
    return host in _TRUSTED_DOMAINS


def check_image_link(image_link: str) -> str:
    """
    Resolve the final URL of an image link and ensure it belongs to a
    trusted domain.

    Parameters
    ----------
    image_link : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The verified final image URL.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if the host is not in the
        whitelist, or if a network error occurs.
    """
    # Basic validation of the input URL
    parsed = urlparse(image_link)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unrecognized scheme '{parsed.scheme}'. Only http and https are allowed.")

    if not parsed.netloc:
        raise ValueError("The provided URL does not contain a valid host.")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not in the list of trusted image hosts.")

    # Resolve any redirects safely, ensuring the final URL is still trusted
    try:
        with requests.Session() as session:
            # Use a short timeout to avoid hanging on bad hosts
            resp = session.get(image_link, allow_redirects=True, timeout=10)
    except requests.RequestException as exc:
        raise ValueError(f"Failed to fetch the image URL: {exc}") from exc

    final_parsed = urlparse(resp.url)
    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(f"Final URL domain '{final_parsed.netloc}' is not trusted after redirects.")

    return resp.url