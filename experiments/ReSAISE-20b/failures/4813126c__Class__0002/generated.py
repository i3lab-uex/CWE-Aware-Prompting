import re
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Trusted image hosting domains (allow any sub‑domain of these)
TRUSTED_DOMAINS = [
    "imgur.com",
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
]

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(domain: str) -> bool:
    """
    Return True if the domain matches any of the trusted domains or a sub‑domain
    thereof.
    """
    return any(domain == td or domain.endswith("." + td) for td in TRUSTED_DOMAINS)


def _validate_url(parsed: "ParseResult") -> None:
    """
    Validate scheme and domain of a parsed URL.
    Raises ValueError if invalid.
    """
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location")

    if not _is_trusted_domain(parsed.netloc.lower()):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")


def verify_image_url(img_url: str) -> str:
    """
    Resolve an image URL, following redirects while ensuring that every
    intermediate and final destination remains within the list of trusted
    image hosting domains.

    Parameters:
        img_url (str): The original URL to verify.

    Returns:
        str: The final resolved URL if all domains are trusted.

    Raises:
        ValueError: If the scheme is unsupported, a domain is untrusted,
                    or any redirect leads to an untrusted domain.
    """
    if not isinstance(img_url, str):
        raise ValueError("img_url must be a string")

    # Initial validation
    parsed = urlparse(img_url)
    _validate_url(parsed)

    # Create a session that will not follow redirects automatically so we
    # can inspect each one.
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3,
                    status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        # Perform a HEAD request to get the final URL without downloading content
        response = session.head(
            img_url,
            allow_redirects=False,  # we will handle redirects manually
            timeout=10,
        )
    except requests.RequestException as exc:
        raise ValueError(f"Failed to reach URL: {exc}") from exc

    # Follow redirects manually, validating each step
    redirect_count = 0
    MAX_REDIRECTS = 10

    while response.is_redirect or response.is_permanent_redirect:
        if redirect_count >= MAX_REDIRECTS:
            raise ValueError("Too many redirects")

        location = response.headers.get("Location")
        if not location:
            raise ValueError("Redirect without Location header")

        # Resolve relative redirects
        redirect_url = requests.compat.urljoin(response.url, location)
        parsed_redirect = urlparse(redirect_url)

        # Validate the redirect URL
        _validate_url(parsed_redirect)

        try:
            response = session.head(
                redirect_url,
                allow_redirects=False,
                timeout=10,
            )
        except requests.RequestException as exc:
            raise ValueError(f"Failed to follow redirect: {exc}") from exc

        redirect_count += 1

    # After all redirects, ensure the final URL domain is still trusted
    final_parsed = urlparse(response.url)
    _validate_url(final_parsed)

    return response.url