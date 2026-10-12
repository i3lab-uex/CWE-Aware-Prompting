import re
from urllib.parse import urlparse, urlunparse, quote_plus

# Define the set of domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "sub.example.com",
    "trusted.org",
}

# Only these schemes are permitted.
ALLOWED_SCHEMES = {"http", "https"}


def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the provided domain or any of its parent domains are in ALLOWED_DOMAINS.
    For example, if 'sub.example.com' is allowed, then 'foo.sub.example.com' should also be allowed.
    """
    # Strip port if present
    domain = domain.split(":")[0].lower()
    for allowed in ALLOWED_DOMAINS:
        if domain == allowed or domain.endswith("." + allowed):
            return True
    return False


def _sanitize_path(path: str) -> str:
    """
    Percent‑encode the path component to avoid traversal attacks.
    """
    # Preserve slashes while encoding other characters
    segments = [quote_plus(segment, safe="") for segment in path.split("/")]
    return "/".join(segments)


def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized absolute URL that is guaranteed to point to an allowed domain.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme, or points to a domain that is not allowed.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is present and allowed
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (e.g., http:// or https://)")
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Ensure a network location (domain) exists
    if not parsed.netloc:
        raise ValueError("URL must include a domain")

    # Validate the domain
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed")

    # Sanitize path and query
    sanitized_path = _sanitize_path(parsed.path)
    sanitized_query = quote_plus(parsed.query, safe="=&")  # keep key/value separators

    # Rebuild the URL
    sanitized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc,
        sanitized_path,
        parsed.params,  # params are rarely used; keep as-is
        sanitized_query,
        ""  # fragment is omitted for redirection safety
    ))

    return sanitized


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(process_user_redirect("https://sub.example.com/../etc/passwd"))
#     except ValueError as e:
#         print(f"Redirect denied: {e}")