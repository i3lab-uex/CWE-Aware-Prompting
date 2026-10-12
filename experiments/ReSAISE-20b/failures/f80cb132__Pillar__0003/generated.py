import re
from urllib.parse import urlparse, ParseResult

# List of domains that are considered safe for redirection.
# Add or remove domains as required by your application policy.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regular expression to validate that the scheme is http or https.
_SCHEME_RE = re.compile(r"^(http|https)$", re.IGNORECASE)


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user supplied URL and return it only if its domain is approved.

    Parameters
    ----------
    url_input : str
        The URL string supplied by the user.

    Returns
    -------
    str
        The validated, safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or its domain
        is not in ``APPROVED_DOMAINS``.
    """
    # Basic validation: ensure the input is a non-empty string
    if not isinstance(url_input, str) or not url_input.strip():
        raise ValueError("URL must be a non-empty string")

    # Parse the URL
    parsed: ParseResult = urlparse(url_input.strip())

    # Ensure that scheme and netloc are present
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and domain")

    # Verify the scheme is http or https
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError("Only HTTP and HTTPS schemes are allowed")

    # Normalize the hostname to lowercase for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check that the hostname ends with one of the approved domains.
    # This allows subdomains of an approved domain to be accepted
    # while preventing arbitrary domains.
    if not any(host == d or host.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure no additional components (e.g., username, password)
    safe_url = parsed._replace(
        username=None,
        password=None,
        fragment="",
    ).geturl()

    return safe_url