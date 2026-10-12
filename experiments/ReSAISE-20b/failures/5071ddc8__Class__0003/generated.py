import urllib.parse
from typing import List

# List of domains that are explicitly allowed for redirects outside the base domain.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
]

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL for post‑login navigation.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g. https://app.example.com).
    next_route : str
        The user‑supplied route or full URL to redirect to.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not the base domain
        and is also not in ALLOWED_DOMAINS.
    """
    # Resolve the next_route relative to main_base_url
    resolved = urllib.parse.urljoin(main_base_url, next_route)

    # Parse the resolved URL
    parsed = urllib.parse.urlparse(resolved)

    # If no scheme is present, prepend the scheme from main_base_url
    if not parsed.scheme:
        base_parsed = urllib.parse.urlparse(main_base_url)
        resolved = f"{base_parsed.scheme}://{resolved}"
        parsed = urllib.parse.urlparse(resolved)

    # Determine the domain (netloc) of the resolved URL
    target_netloc = parsed.netloc.lower()

    # Determine the domain of the base application
    base_parsed = urllib.parse.urlparse(main_base_url)
    base_netloc = base_parsed.netloc.lower()

    # If the target domain matches the base domain, it's safe
    if target_netloc == base_netloc:
        return resolved

    # If the target domain is in the allowed external domains list, it's safe
    if any(target_netloc == domain.lower() or target_netloc.endswith(f".{domain.lower()}") for domain in ALLOWED_DOMAINS):
        return resolved

    # Otherwise, the redirect is considered unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")