import re
from urllib.parse import urlparse, urlunparse

# List of domains that are allowed for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.net",
}

# Regular expression to validate the scheme and avoid fragments or query parameters that
# might be used maliciously (e.g., javascript:).
_SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)


def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user-supplied URL and ensure it points to an approved domain.

    Parameters
    ----------
    input_url : str
        The URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in ``APPROVED_DOMAINS`` or if the scheme is
        not HTTP/HTTPS.
    """
    # Parse the URL. ``urlparse`` returns a ParseResult with components.
    parsed = urlparse(input_url)

    # Reject URLs that don't have a scheme or host.
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and host")

    # Ensure the scheme is HTTP or HTTPS only.
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError("Only HTTP/HTTPS schemes are allowed")

    # Normalize the domain to lowercase for comparison.
    host = parsed.hostname.lower() if parsed.hostname else ""

    # The host must match one of the approved domains exactly or as a subdomain.
    if not any(
        host == domain or host.endswith("." + domain)
        for domain in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Rebuild the URL without any fragment or query to avoid
    # unintended side effects (e.g., JS in the fragment).
    safe_parsed = parsed._replace(fragment="", query="")
    return urlunparse(safe_parsed)


# Example usage:
if __name__ == "__main__":
    try:
        safe_url = validate_redirect_url("https://sub.example.com/path?param=1#frag")
        print(f"Safe URL: {safe_url}")
    except ValueError as exc:
        print(f"Invalid redirect: {exc}")