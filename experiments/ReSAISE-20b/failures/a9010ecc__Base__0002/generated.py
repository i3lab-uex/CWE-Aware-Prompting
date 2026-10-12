import urllib.parse
from typing import List

# Predefined list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    # add more allowed domains here
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g. "https://app.example.com").
    redirect_param : str
        URL path or full URL provided by the user for redirection.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or not in ALLOWED_DOMAINS.
    """
    # Normalize base URL: ensure it ends with a slash for relative joins
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    if parsed_redirect.scheme and parsed_redirect.netloc:
        # Absolute URL provided by the user
        domain = parsed_redirect.hostname.lower()
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect to external domain '{domain}' is not allowed.")
        # Use the absolute URL as-is (ensure it's safe by checking scheme)
        if parsed_redirect.scheme not in {"http", "https"}:
            raise ValueError("Only http/https schemes are allowed for external redirects.")
        return redirect_param

    # Relative path or query
    if parsed_redirect.netloc:
        # Netloc should be empty for relative URLs; reject otherwise
        raise ValueError("Relative redirects must not contain a netloc.")
    # Ensure the path starts with '/'
    rel_path = parsed_redirect.path
    if not rel_path.startswith("/"):
        rel_path = f"/{rel_path}"
    # Preserve query and fragment if present
    query = parsed_redirect.query
    fragment = parsed_redirect.fragment

    # Build the final URL using urljoin to avoid path traversal issues
    joined = urllib.parse.urljoin(base, rel_path)
    if query:
        joined += f"?{query}"
    if fragment:
        joined += f"#{fragment}"

    # Final sanity check: the resulting URL must start with app_base_url
    if not joined.startswith(app_base_url.rstrip("/")):
        raise ValueError("Redirect URL resolves outside the application base domain.")
    return joined