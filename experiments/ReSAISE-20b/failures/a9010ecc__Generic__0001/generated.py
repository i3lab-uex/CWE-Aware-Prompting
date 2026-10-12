import urllib.parse

# Example list of allowed external domains. In a real application this should be configured
# securely and not hard‑coded.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedsite.org",
    "secure.example.net"
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after successful login.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g. "https://app.example.com/").
    redirect_param : str
        User supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or is an external URL
        that is not on the ALLOWED_DOMAINS list.
    """
    # Normalise base URL
    parsed_base = urllib.parse.urlparse(app_base_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base application URL")

    # If redirect_param looks like an absolute URL, validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_param)
    if parsed_redirect.scheme in {"http", "https"} and parsed_redirect.netloc:
        # External absolute URL
        domain = parsed_redirect.netloc.split(":")[0].lower()
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect URL domain '{domain}' is not allowed")
        # Return the absolute URL as-is
        return redirect_param

    # Otherwise treat it as a relative path
    # Ensure it starts with a slash to avoid ambiguous resolution
    if not redirect_param.startswith("/"):
        redirect_param = "/" + redirect_param

    # Join relative path to base URL
    full_url = urllib.parse.urljoin(app_base_url, redirect_param)

    # Validate that the resulting URL stays within the same domain
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc.lower() != parsed_base.netloc.lower():
        raise ValueError("Redirect URL escapes the base domain")

    return full_url