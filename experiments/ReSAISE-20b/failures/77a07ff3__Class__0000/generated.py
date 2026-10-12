import urllib.parse
from typing import List

# A list of approved domains.  In a real application this might be loaded
# from configuration or an environment variable.
APPROVED_DOMAINS: List[str] = [
    "example.com",
    "trusted-site.org",
    "secure.example.net"
]

def _canonical_domain(netloc: str) -> str:
    """
    Return the hostname part of a netloc, lower‑cased and without any port.
    """
    host = netloc.split(":")[0].lower()
    return host

def process_url_redirect(input_url: str) -> str:
    """
    Validate a user supplied URL and return it if its domain is approved.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        A validated, safe‑to‑use URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, does not contain a scheme or if its domain
        is not in :data:`APPROVED_DOMAINS`.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    # Parse the URL
    parsed = urllib.parse.urlparse(input_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    # Reject URLs with relative paths or fragments that might lead to
    # unintended navigation.
    if parsed.fragment:
        raise ValueError("URL must not contain a fragment")

    # Canonicalise the host and compare against approved list
    host = _canonical_domain(parsed.netloc)
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Rebuild the URL to ensure no unexpected components slip through
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,  # preserve query string if any
            ""   # no fragment allowed
        )
    )

    return safe_url