import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains (can be extended as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
}

# Regular expression to ensure only http or https schemes are allowed
_SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)


def user_defined_redirect(redirect_url: str) -> str:
    """
    Sanitize and validate a user-provided URL for redirection.

    Parameters
    ----------
    redirect_url : str
        The URL supplied by the user to which we may redirect.

    Returns
    -------
    str
        The sanitized absolute URL that is safe to use for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        or its domain is not in :data:`ALLOWED_DOMAINS`.
    """
    if not redirect_url:
        raise ValueError("Redirect URL must not be empty")

    parsed = urlparse(redirect_url)

    # Reject URLs without a scheme or with an unsafe scheme
    if not parsed.scheme:
        raise ValueError("Redirect URL must include a scheme (http or https)")
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs with no netloc (e.g., relative paths or data: URIs)
    if not parsed.netloc:
        raise ValueError("Redirect URL must be absolute and contain a domain")

    # Normalize the domain to lower case for comparison
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Check that the domain is in the allowed list.
    # Allow subdomains of any allowed domain as a simple policy.
    if not any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not permitted for redirection")

    # Reconstruct a clean URL, stripping any fragment
    safe_parsed = parsed._replace(fragment="")
    return urlunparse(safe_parsed)


# Example usage (for testing purposes only; remove or guard in production)
if __name__ == "__main__":
    try:
        print(user_defined_redirect("https://sub.example.com/path?query=1"))
    except ValueError as e:
        print(f"Redirect rejected: {e}")