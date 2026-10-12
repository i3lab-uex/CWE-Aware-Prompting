import re
from urllib.parse import urlparse, urljoin

import requests


# List of trusted image hosting domains (add more as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "imgur.com",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(host: str) -> bool:
    """
    Return True if the host matches one of the trusted domains.
    The check is case‑insensitive and allows subdomains when a base domain
    is explicitly listed.
    """
    host = host.lower()
    for trusted in TRUSTED_DOMAINS:
        if host == trusted or host.endswith("." + trusted):
            return True
    return False


def verify_image_url(img_url: str) -> str:
    """
    Verify that the supplied image URL points to a trusted domain and
    return the final resolved URL after following redirects.

    Parameters
    ----------
    img_url : str
        The image URL to verify.

    Returns
    -------
    str
        The verified, final image URL after following redirects.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, or if any host in the
        redirect chain is untrusted.
    """
    # Parse and validate scheme
    parsed = urlparse(img_url)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate initial host
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    session = requests.Session()
    # Don't automatically follow redirects; we want to inspect each hop
    session.max_redirects = 5

    current_url = img_url
    for _ in range(6):  # allow up to 5 redirects + the initial request
        try:
            resp = session.head(current_url, allow_redirects=False, timeout=5)
        except requests.RequestException as exc:
            raise ValueError(f"Failed to resolve URL: {exc}") from exc

        # If status code indicates a redirect, process it
        if resp.is_redirect or resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("Location")
            if not location:
                raise ValueError(f"Redirect without Location header from {current_url}")

            # Resolve relative redirects
            next_url = urljoin(current_url, location)
            parsed_next = urlparse(next_url)

            # Validate scheme and domain of the redirect target
            if parsed_next.scheme.lower() not in ALLOWED_SCHEMES:
                raise ValueError(f"Redirect to unsupported scheme: {parsed_next.scheme}")
            if not _is_trusted_domain(parsed_next.netloc):
                raise ValueError(f"Redirect to untrusted domain: {parsed_next.netloc}")

            current_url = next_url
        else:
            # Final URL reached; ensure it's still trusted
            parsed_final = urlparse(current_url)
            if not _is_trusted_domain(parsed_final.netloc):
                raise ValueError(f"Final URL host untrusted: {parsed_final.netloc}")
            return current_url

    # If we exit the loop, too many redirects
    raise ValueError("Too many redirects while resolving image URL")