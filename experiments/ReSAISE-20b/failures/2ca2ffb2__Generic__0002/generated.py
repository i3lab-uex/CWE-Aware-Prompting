import re
from urllib.parse import urlparse

import requests


# List of approved image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "pbs.twimg.com",
    "flickr.com",
    "staticflickr.com",
    "cdn.discordapp.com",
    "i.redd.it",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(host: str) -> bool:
    """
    Check if the host ends with one of the trusted domains.
    The check is case‑insensitive and allows subdomains
    that are explicitly listed in _TRUSTED_DOMAINS.
    """
    host = host.lower()
    return any(host == d or host.endswith("." + d) for d in _TRUSTED_DOMAINS)


def fetch_image_url(url: str, timeout: float = 10.0) -> str:
    """
    Resolve an image URL to its final location after following redirects
    and ensure the domain is from a trusted image hosting service.

    Parameters
    ----------
    url : str
        The original URL of the image.
    timeout : float, optional
        Maximum number of seconds to wait for a response.

    Returns
    -------
    str
        The verified, final image URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, or if after following redirects
        the domain is not in the trusted list.
    """
    # Basic validation of scheme and host
    parsed = urlparse(url)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Resolve redirects securely
    try:
        session = requests.Session()
        # Use HEAD first to avoid downloading large images when unnecessary
        resp = session.head(url, allow_redirects=True, timeout=timeout)
    except requests.RequestException as exc:
        raise ValueError(f"Failed to fetch URL: {exc}") from exc

    # If HEAD returned 405/403, fall back to GET
    if resp.status_code in {405, 403}:
        try:
            resp = session.get(url, allow_redirects=True, timeout=timeout)
        except requests.RequestException as exc:
            raise ValueError(f"Failed to fetch URL: {exc}") from exc

    final_url = resp.url
    final_parsed = urlparse(final_url)

    if final_parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Redirected to unsupported scheme: {final_parsed.scheme}")

    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(f"Redirected to untrusted domain: {final_parsed.netloc}")

    return final_url