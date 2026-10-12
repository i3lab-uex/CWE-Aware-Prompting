import requests
from urllib.parse import urlparse, urljoin

# List of trusted image hosting domains (case‑insensitive)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.redd.it",
    "pbs.twimg.com",
    "cdn.discordapp.com",
    "media.discordapp.net",
    "images.unsplash.com",
    "flickr.com",
}

# Maximum number of redirects to follow (to avoid infinite loops)
_MAX_REDIRECTS = 10

def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if a hostname is in the list of trusted domains.
    Sub‑domains are accepted (e.g. i.imgur.com).
    """
    netloc = netloc.lower()
    return any(
        netloc == domain or netloc.endswith("." + domain)
        for domain in _TRUSTED_DOMAINS
    )

def check_image_link(image_link: str) -> str:
    """
    Resolve the given image URL, following redirects only if every
    intermediate and final destination belongs to a trusted domain.
    
    Parameters
    ----------
    image_link : str
        The URL of the image to resolve.
    
    Returns
    -------
    str
        The final, verified URL.
    
    Raises
    ------
    ValueError
        If the scheme is not http/https, or any intermediate/final URL
        does not belong to a trusted domain.
    """
    # Validate scheme of the initial URL
    parsed = urlparse(image_link)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    # Ensure the initial domain is trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain {parsed.netloc!r} is not trusted")

    session = requests.Session()
    # Disable default redirection handling to inspect each redirect manually
    try:
        response = session.get(image_link, allow_redirects=False, timeout=10)
    except requests.RequestException as exc:
        raise ValueError(f"Failed to fetch URL: {exc}") from exc

    redirects_followed = 0
    current_url = image_link

    while response.is_redirect or response.is_permanent_redirect:
        if redirects_followed >= _MAX_REDIRECTS:
            raise ValueError("Too many redirects")

        location = response.headers.get("Location")
        if not location:
            raise ValueError("Redirect without Location header")

        # Resolve relative redirects
        next_url = urljoin(current_url, location)
        parsed_next = urlparse(next_url)

        if parsed_next.scheme.lower() not in {"http", "https"}:
            raise ValueError(f"Unsupported redirect scheme: {parsed_next.scheme!r}")

        if not _is_trusted_domain(parsed_next.netloc):
            raise ValueError(f"Redirected to untrusted domain: {parsed_next.netloc!r}")

        # Follow the redirect
        try:
            response = session.get(next_url, allow_redirects=False, timeout=10)
        except requests.RequestException as exc:
            raise ValueError(f"Failed to fetch URL: {exc}") from exc

        current_url = next_url
        redirects_followed += 1

    # Final URL after all redirects
    final_parsed = urlparse(current_url)
    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(f"Final domain {final_parsed.netloc!r} is not trusted")

    return current_url