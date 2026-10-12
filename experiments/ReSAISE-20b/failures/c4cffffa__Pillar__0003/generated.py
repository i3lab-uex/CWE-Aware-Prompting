import urllib.parse

# Allowed domains for the return URL (example values)
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (may already contain query parameters).
    user_identifier : str
        Unique identifier for the user.
    redirect_back_url : str
        URL to return to after SSO completion.

    Returns
    -------
    str
        The fully qualified SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the redirect back URL domain
    parsed_back = urllib.parse.urlparse(redirect_back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("redirect_back_url must be a valid absolute URL")

    domain = parsed_back.netloc.split(":")[0]  # ignore port
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters
    params = {
        "user_id": user_identifier,
        "return_to": redirect_back_url
    }
    encoded_params = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=")

    # Parse the SSO service URL to preserve existing components
    parsed_sso = urllib.parse.urlparse(sso_service_url)

    # Merge existing query with new parameters
    if parsed_sso.query:
        merged_query = f"{parsed_sso.query}&{encoded_params}"
    else:
        merged_query = encoded_params

    # Reconstruct the full URL
    sso_redirect = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            merged_query,
            parsed_sso.fragment
        )
    )

    return sso_redirect