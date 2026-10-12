import re
from urllib.parse import urlparse, urlunparse

# Define a set of domains that are allowed for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "www.example.com",
    "trusted.org",
    # Add more safe domains here
}

# Regular expression to detect any fragment that could lead to SSRF.
_FRAGMENT_RE = re.compile(r"[#\?]")

def user_defined_redirect(redirect_url: str) -> str:
    """
    Validate and sanitize a user-provided URL for safe redirection.

    Parameters
    ----------
    redirect_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is guaranteed to point to an allowed domain.

    Raises
    ------
    ValueError
        If the URL is malformed, does not contain a scheme, or its domain is not in ALLOWED_DOMAINS.
    """
    # Basic sanity check: the URL must contain a scheme and netloc
    parsed = urlparse(redirect_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and domain")

    # Normalise the netloc to lowercase for comparison
    host = parsed.hostname.lower()
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Remove any fragment or query to avoid unintended side effects
    cleaned = parsed._replace(query="", fragment="")

    # Reconstruct the sanitized URL
    return urlunparse(cleaned)

# Example usage (for testing purposes only):
if __name__ == "__main__":
    try:
        print(user_defined_redirect("https://example.com/path?foo=bar#section"))
    except ValueError as e:
        print(f"Redirect error: {e}")