import urllib.parse

# Example set of allowed domains; replace with real values as needed.
ALLOWED_RETURN_DOMAINS = {"example.com", "trustedsite.org"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    user_ref : str
        Unique identifier for the user (e.g. a UUID or username).
    back_url : str
        URL to return to after the SSO process.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain of `back_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the back_url to extract its domain
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError(f"Invalid back_url: '{back_url}'")

    # Extract the hostname (domain) and compare against allowed list
    back_domain = parsed_back.hostname.lower()
    if back_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain '{back_domain}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters, ensuring proper URL‑encoding
    params = {
        "user_ref": user_ref,
        "back_url": back_url,  # The SSO service should be able to decode this
    }
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)

    # Ensure the base SSO service URL ends with a path separator if needed
    sso_base = sso_service.rstrip("?")  # strip any stray question marks

    # Combine base URL and query string
    redirect_url = f"{sso_base}?{encoded_params}"
    return redirect_url