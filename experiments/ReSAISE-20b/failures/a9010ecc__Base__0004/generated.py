import urllib.parse

# List of external domains that are allowed to be redirected to.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add other trusted domains here
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://myapp.com").
    redirect_param : str
        User-provided path or URL to redirect to.

    Returns
    -------
    str
        Fully-qualified, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an allowed external domain.
    """
    # Ensure base URL ends with a slash for proper urljoin behaviour
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Parse the user supplied redirect
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # If the redirect is a full URL (has scheme and netloc)
    if parsed_redirect.scheme in ("http", "https") and parsed_redirect.netloc:
        # Normalize netloc (remove port if present)
        netloc = parsed_redirect.netloc.split(":")[0].lower()
        # Allow only if domain is in the whitelist
        if netloc not in ALLOWED_DOMAINS:
            raise ValueError(f"Untrusted redirect domain: {netloc}")
        # Build the final URL exactly as supplied
        final_url = urllib.parse.urlunparse(parsed_redirect)
    else:
        # Treat as a relative path; clean it and join with base
        cleaned_path = urllib.parse.urljoin(base, redirect_param)
        # Ensure the resulting URL is still under the application domain
        parsed_cleaned = urllib.parse.urlparse(cleaned_path)
        if not cleaned_path.startswith(app_base_url):
            raise ValueError("Redirect path escapes the application domain")
        final_url = cleaned_path

    return final_url