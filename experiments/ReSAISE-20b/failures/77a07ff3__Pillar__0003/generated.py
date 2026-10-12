import re
from urllib.parse import urlparse, urlunparse

# Pre‑approved domains for safe redirection
APPROVED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "safe-domain.net",
}

# Regular expression to validate the scheme (http or https)
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, missing a scheme, or its domain is not approved.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Ensure the URL contains a scheme
    if not _SCHEME_RE.match(input_url):
        raise ValueError("URL must start with http:// or https://")

    # Parse the URL
    parsed = urlparse(input_url)

    # Reject URLs with empty netloc (e.g., relative paths)
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalize the netloc to lowercase for comparison
    domain = parsed.netloc.lower()

    # Strip port numbers (e.g., example.com:8080) before comparison
    domain = domain.split(":")[0]

    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it uses only allowed components
    safe_url = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url