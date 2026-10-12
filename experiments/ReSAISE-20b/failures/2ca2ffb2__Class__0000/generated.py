import re
from urllib.parse import urlparse, urlunparse

import requests

# List of domains that are allowed to serve images
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trusted.org",
    # Add more trusted domains here
}

# Regular expression to match a valid HTTP/HTTPS scheme
SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)


def fetch_image_url(url: str) -> str:
    """
    Resolve an image URL and ensure the final destination is on a trusted domain.

    Parameters
    ----------
    url : str
        The initial URL of the image to resolve.

    Returns
    -------
    str
        The final, resolved URL that points to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP/HTTPS, or if the final resolved domain is not trusted.
    """
    # Validate that the URL has a scheme and a netloc
    parsed = urlparse(url)
    if not SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Perform the request with no proxy usage to avoid unintended forwarding
    session = requests.Session()
    session.trust_env = False  # ignore environment proxies
    try:
        resp = session.get(url, allow_redirects=True, timeout=10)
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {e}") from e

    # Extract the final URL after redirects
    final_url = resp.url
    final_parsed = urlparse(final_url)

    # Ensure the final domain is trusted
    if final_parsed.netloc not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {final_parsed.netloc!r}")

    # Normalise the URL (e.g., remove fragments)
    cleaned = final_parsed._replace(fragment="")
    return urlunparse(cleaned)


# Example usage (commented out – remove or modify as needed)
# if __name__ == "__main__":
#     try:
#         verified = fetch_image_url("https://images.example.com/photo.jpg")
#         print(f"Verified URL: {verified}")
#     except ValueError as exc:
#         print(f"Validation error: {exc}")