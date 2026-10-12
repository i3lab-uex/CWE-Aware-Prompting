import re
from urllib.parse import urlparse, urlunparse

import requests


# Trusted domains – add any additional image hosting services here.
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "static.wixstatic.com",
    "cdn2.thecatapi.com",
}


def _is_trusted_domain(domain: str) -> bool:
    """Check whether the domain (or any of its parent domains) is trusted."""
    # Normalise subdomains: only the last two labels are checked
    return any(domain == d or domain.endswith("." + d) for d in _TRUSTED_DOMAINS)


def verify_image_url(img_url: str, timeout: float = 5.0) -> str:
    """
    Resolve an image URL and ensure that the final destination is hosted on a
    trusted domain.

    Parameters
    ----------
    img_url : str
        The original image URL to verify.
    timeout : float, optional
        Request timeout in seconds.

    Returns
    -------
    str
        The final resolved URL if it is on a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, if it does not resolve to a trusted
        domain, or if any redirect leads to an untrusted domain.
    """
    # Basic validation of the input URL
    parsed = urlparse(img_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # The URL must be absolute
    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    # Resolve the URL, following redirects, but guard against infinite loops
    session = requests.Session()
    try:
        response = session.head(
            img_url,
            allow_redirects=True,
            timeout=timeout,
            headers={"User-Agent": "ImageVerifier/1.0"},
        )
    except requests.RequestException as exc:
        raise ValueError(f"Unable to fetch URL: {exc}") from exc

    # Inspect each step in the redirect chain
    for resp in response.history:
        location = resp.headers.get("Location")
        if not location:
            continue
        redirect_parsed = urlparse(location)
        if redirect_parsed.scheme.lower() not in {"http", "https"}:
            raise ValueError(f"Redirect to unsupported scheme: {redirect_parsed.scheme!r}")
        if not _is_trusted_domain(redirect_parsed.netloc):
            raise ValueError(f"Redirect leads to untrusted domain: {redirect_parsed.netloc!r}")

    # Finally check the destination
    final_url = response.url
    final_parsed = urlparse(final_url)
    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(f"Final URL is not on a trusted domain: {final_parsed.netloc!r}")

    # Reconstruct the URL to ensure it is normalized
    cleaned = final_parsed._replace(fragment="", query="")  # strip fragment & query if not needed
    return urlunparse(cleaned)