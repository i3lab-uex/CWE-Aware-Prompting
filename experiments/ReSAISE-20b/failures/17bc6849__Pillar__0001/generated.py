import re
from urllib.parse import urlparse, urljoin

# Domains considered safe for external redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    forward_param : str
        URL path or address the user wants to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Parse the forward parameter
    parsed = urlparse(forward_param)

    # If the URL is absolute, validate its domain
    if parsed.scheme and parsed.netloc:
        # Ensure the netloc is in the allowed list
        if parsed.hostname not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{parsed.hostname}' is not allowed for redirection.")
        # Return the absolute URL as is (already safe)
        return forward_param

    # If it's a relative path, ensure it does not contain fragments or query that could lead to open redirect
    if re.search(r"[<>\"'`]", forward_param):
        raise ValueError("Forward parameter contains invalid characters.")

    # Build absolute URL by joining with the application home
    redirect_url = urljoin(app_home_url, forward_param)

    # Final validation: the resulting URL must start with app_home_url or be in ALLOWED_DOMAINS
    parsed_redirect = urlparse(redirect_url)
    if not (parsed_redirect.netloc == urlparse(app_home_url).netloc or
            parsed_redirect.hostname in ALLOWED_DOMAINS):
        raise ValueError("Redirect URL is not within the allowed domain scope.")

    return redirect_url