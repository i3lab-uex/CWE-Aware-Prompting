import urllib.parse

# Example set of allowed domains for the redirect back URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "app.example.org"}

def build_sso_redirect_link(sso_service_url: str,
                            user_identifier: str,
                            redirect_back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g., "https://sso.example.com/login").
    user_identifier : str
        Unique identifier of the user to be passed to the SSO service.
    redirect_back_url : str
        URL that the SSO service should redirect to after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL with encoded query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect_back_url domain
    parsed_redirect = urllib.parse.urlparse(redirect_back_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_back_url must be a valid absolute URL")

    # Normalize domain (strip port if present)
    domain = parsed_redirect.hostname or ""
    if domain.lower() not in (d.lower() for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Ensure the SSO service URL is absolute
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("sso_service_url must be a valid absolute URL")

    # Construct query parameters
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url
    }
    query_string = urllib.parse.urlencode(params, safe=":/")  # keep :// in redirect_back

    # Combine base URL with query string
    sso_redirect_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        query_string,
        parsed_sso.fragment
    ))

    return sso_redirect_url