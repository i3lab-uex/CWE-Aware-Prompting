import urllib.parse

# Example list of safe external domains
ALLOWED_DOMAINS = ["example.com", "trusted.org"]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Build a secure redirect URL by concatenating the base application URL
    with a user-supplied forward parameter.

    Args:
        app_home_url: Base URL of the application (e.g. "https://myapp.com").
        forward_param: Path or full URL the user wishes to navigate to after login.

    Returns:
        A fully-qualified redirect URL.

    Raises:
        ValueError: If the resulting URL is not within the base domain or
                    an allowed external domain.
    """
    # Ensure app_home_url ends with a slash for correct joining
    if not app_home_url.endswith("/"):
        base = f"{app_home_url}/"
    else:
        base = app_home_url

    # Parse the forward parameter
    parsed_forward = urllib.parse.urlparse(forward_param)

    # If it's an absolute URL, verify domain
    if parsed_forward.scheme and parsed_forward.netloc:
        # Normalise the netloc (lowercase, strip port)
        domain = parsed_forward.netloc.split(":")[0].lower()
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{domain}' is not allowed for redirection.")
        # Build final URL directly
        redirect_url = forward_param
    else:
        # Relative path: join with base and ensure it stays within the app domain
        redirect_url = urllib.parse.urljoin(base, forward_param)

        # Verify that the resulting URL is still under app_home_url
        parsed_redirect = urllib.parse.urlparse(redirect_url)
        base_parsed = urllib.parse.urlparse(app_home_url)

        if parsed_redirect.netloc.lower() != base_parsed.netloc.lower():
            raise ValueError("Redirect URL escapes the application domain.")

        # Prevent directory traversal by normalising path
        normalized_path = urllib.parse.urljoin("/", parsed_redirect.path)
        if ".." in normalized_path.split("/"):
            raise ValueError("Redirect URL contains forbidden path traversal.")

    return redirect_url