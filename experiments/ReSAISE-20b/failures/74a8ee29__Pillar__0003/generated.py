import urllib.parse
from typing import List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# List of domains that are considered trusted image hosts.
TRUSTED_DOMAINS: List[str] = [
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    # Add more trusted domains as needed.
]


def _is_trusted_domain(netloc: str) -> bool:
    """
    Return True if the hostname part of a URL is in TRUSTED_DOMAINS.
    """
    # Normalize subdomains: strip port if present
    host = netloc.split(":")[0].lower()
    return host in TRUSTED_DOMAINS


def _validate_scheme(parsed: urllib.parse.ParseResult) -> None:
    """
    Ensure the URL uses an accepted scheme.
    Raise ValueError if not.
    """
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")


def _resolve_final_url(url: str, timeout: float = 10.0) -> str:
    """
    Resolve the final URL after following redirects.
    Uses a session that is closed immediately after use to avoid resource leaks
    (CWE‑664 mitigation).
    """
    # Configure a session with retry logic to handle transient network errors.
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5,
                    status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        # Use HEAD to avoid downloading the image data.
        response = session.head(url, allow_redirects=True,
                                timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"Failed to resolve URL {url!r}: {exc}") from exc
    finally:
        session.close()

    return response.url


def check_image_link(image_link: str) -> str:
    """
    Validate an image URL and return the final resolved URL if it points to a
    trusted domain.

    Parameters:
        image_link (str): The original URL of the image.

    Returns:
        str: The final URL after following redirects, guaranteed to belong
             to a trusted domain.

    Raises:
        ValueError: If the URL uses an unsupported scheme, cannot be resolved,
                    or does not belong to a trusted domain.
    """
    if not isinstance(image_link, str):
        raise ValueError("image_link must be a string")

    parsed = urllib.parse.urlparse(image_link)
    _validate_scheme(parsed)

    # Resolve redirects to get the final URL.
    final_url = _resolve_final_url(image_link)

    # Check that the final domain is trusted.
    final_parsed = urllib.parse.urlparse(final_url)
    if not _is_trusted_domain(final_parsed.netloc):
        raise ValueError(f"Untrusted domain in final URL: {final_parsed.netloc!r}")

    return final_url