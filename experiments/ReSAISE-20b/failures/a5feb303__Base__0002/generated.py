import urllib.parse

# Predefined list of domains that are considered safe for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "myapp.local",
}

def process_user_redirect(input_url: str) -> str:
    """
    Sanitize a user‑provided URL and ensure it points to an allowed domain.
    
    Parameters
    ----------
    input_url : str
        The URL supplied by the user that we wish to redirect to.

    Returns
    -------
    str
        The sanitized, fully‑qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not belong to one of the allowed domains.
    """
    # Parse the input URL
    parsed = urllib.parse.urlparse(input_url)

    # Ensure a scheme is present; default to https if missing
    scheme = parsed.scheme or "https"

    # Resolve the hostname (netloc may include port)
    netloc = parsed.netloc
    if not netloc:
        # Handle URLs like "example.com/path" where the scheme is omitted
        if parsed.path:
            # Treat the first path segment as the hostname
            parts = parsed.path.split("/", 1)
            netloc = parts[0]
            path = "/" + parts[1] if len(parts) > 1 else "/"
        else:
            raise ValueError("URL must contain a hostname")

    # Separate host and port
    host, _, port = netloc.partition(":")
    host = host.lower()

    # Check if the hostname is in the allowed list
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for redirection")

    # Reconstruct the sanitized URL
    sanitized = urllib.parse.urlunparse(
        (
            scheme,
            netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized

# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        safe_url = process_user_redirect("https://example.com/welcome?user=123")
        print(f"Safe redirect URL: {safe_url}")
    except ValueError as e:
        print(e)