import urllib.parse
from typing import List

# Approved domains – modify as needed
APPROVED_DOMAINS: List[str] = [
    "example.com",
    "trustedsite.org",
    "secure.example.net",
]

def _normalize_domain(domain: str) -> str:
    """
    Normalize a domain by removing any leading 'www.' and converting to lowercase.
    """
    return domain.lower().lstrip("www.")


def _extract_base_domain(url: str) -> str:
    """
    Extract the base domain (registered domain + suffix) from a URL.
    """
    parsed = urllib.parse.urlparse(url)
    # Handle URLs like "http://sub.example.com:8080/path"
    host = parsed.hostname or ""
    return _normalize_domain(host)


def validate_redirect_url(input_url: str) -> str:
    """
    Validate that the user-supplied URL belongs to an approved domain.

    Parameters
    ----------
    input_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The validated, normalized URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if the scheme is invalid.
    """
    # Basic sanitation
    input_url = input_url.strip()

    parsed = urllib.parse.urlparse(input_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    base_domain = _extract_base_domain(input_url)
    if not any(base_domain == _normalize_domain(approved) for approved in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{base_domain}' is not approved for redirection")

    # Rebuild the URL to ensure consistent formatting
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return safe_url