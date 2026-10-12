import urllib.parse
import urllib.request

# A set of domains that are considered trusted image hosts.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "picsum.photos",
    "placekitten.com",
}

def verify_image_url(img_url: str) -> str:
    """
    Verify that an image URL belongs to a trusted domain and return the final
    URL after following any redirects.

    Parameters
    ----------
    img_url : str
        The original image URL to verify and resolve.

    Returns
    -------
    str
        The final resolved URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the scheme is not HTTP/HTTPS or if the domain is not in TRUSTED_DOMAINS.
    """
    # Parse the URL and validate scheme
    parsed = urllib.parse.urlparse(img_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unrecognized URL scheme: {parsed.scheme}")

    # Normalise the netloc (remove port if present)
    host = parsed.hostname
    if host is None:
        raise ValueError("URL does not contain a hostname")

    # Check against the trusted domain list
    if host.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not trusted")

    # Follow redirects to get the final URL
    try:
        with urllib.request.urlopen(img_url, timeout=10) as response:
            final_url = response.geturl()
    except Exception as exc:
        raise ValueError(f"Failed to resolve URL: {exc}") from exc

    # Ensure the final host is still trusted (redirect might lead elsewhere)
    final_parsed = urllib.parse.urlparse(final_url)
    if final_parsed.hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(
            f"Redirected to untrusted domain: {final_parsed.hostname}"
        )

    return final_url