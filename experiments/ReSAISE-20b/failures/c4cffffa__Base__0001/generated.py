import urllib.parse

# Set of domains that are allowed as return URLs
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service.
    user_identifier : str
        Unique identifier for the user to be sent to the SSO service.
    redirect_back_url : str
        URL where the user should be sent after authentication.

    Returns
    -------
    str
        Full SSO redirect URL containing the user identifier and return URL.

    Raises
    ------
    ValueError
        If `redirect_back_url` does not belong to an allowed domain.
    """
    # Validate that the return URL is from an allowed domain
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("Redirect URL must be absolute and contain a scheme and netloc.")
    # Extract hostname (without port)
    host = parsed_return.hostname or ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed.")

    # Prepare query parameters
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url
    }
    query_string = urllib.parse.urlencode(params)

    # Build the final URL safely
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    # Preserve existing components of sso_service_url
    new_query = urllib.parse.urlencode(
        dict(urllib.parse.parse_qsl(parsed_sso.query))
    )
    # Append our parameters
    if new_query:
        combined_query = f"{new_query}&{query_string}"
    else:
        combined_query = query_string

    final_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path or "",
        parsed_sso.params,
        combined_query,
        parsed_sso.fragment
    ))
    return final_url