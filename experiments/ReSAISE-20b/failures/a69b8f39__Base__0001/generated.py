import urllib.parse

# Domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        The base URL of the SSO service.
    user_ref : str
        Unique identifier for the user (passed as a query param).
    back_url : str
        URL to redirect back after the SSO flow.

    Returns
    -------
    str
        The fully-formed redirect URL.

    Raises
    ------
    ValueError
        If ``back_url``'s domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the back_url to validate its domain.
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("back_url must be an absolute URL")

    domain = parsed_back.hostname
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for return URLs")

    # Parse the SSO service URL and ensure it has a scheme.
    parsed_sso = urllib.parse.urlparse(sso_service)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("sso_service must be an absolute URL")

    # Build query parameters.
    query_params = {
        "user_ref": user_ref,
        "return_url": back_url,  # will be percent‑encoded by urlencode
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL.
    sso_redirect = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        encoded_query,
        parsed_sso.fragment
    ))

    return sso_redirect