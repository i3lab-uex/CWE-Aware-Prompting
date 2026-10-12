import urllib.parse
from typing import List

# Domains that are considered safe for external redirects.
SAFE_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URI based on the supplied ``next_path``.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. ``https://app.example.com``).
    next_path : str
        The path or full URL the user wants to be redirected to after login.

    Returns
    -------
    str
        The fully qualified redirect URL that is guaranteed to be within the
        application domain or one of the ``SAFE_DOMAINS``.

    Raises
    ------
    ValueError
        If the resolved redirect URL points to a domain that is not part of the
        application or an allowed external domain.
    """
    # Parse the base URL once for reuse
    primary_parsed = urllib.parse.urlparse(primary_url)

    # Resolve the next path against the primary URL
    resolved = urllib.parse.urljoin(primary_url, next_path)

    # Parse the resulting URL to inspect its components
    resolved_parsed = urllib.parse.urlparse(resolved)

    # If the scheme or netloc is missing, treat it as relative and rebuild
    if not resolved_parsed.scheme or not resolved_parsed.netloc:
        # Ensure we don't accidentally create a relative URL that escapes the app
        resolved_parsed = urllib.parse.urlparse(
            urllib.parse.urljoin(primary_url, next_path)
        )

    # Normalise netloc by stripping port numbers for comparison
    def _normalize_netloc(netloc: str) -> str:
        return netloc.split(":")[0].lower()

    primary_netloc = _normalize_netloc(primary_parsed.netloc)
    resolved_netloc = _normalize_netloc(resolved_parsed.netloc)

    # Check if the redirect points back to the application
    if resolved_netloc == primary_netloc:
        # All good – return the fully constructed URL
        return resolved

    # Otherwise, ensure it is an explicitly allowed external domain
    if resolved_netloc in {d.lower() for d in SAFE_DOMAINS}:
        return resolved

    # If we reach here, the redirect is unsafe
    raise ValueError(
        f"Redirect URL '{resolved}' is not allowed: "
        f"netloc '{resolved_netloc}' does not match application domain "
        f"or any safe external domain."
    )