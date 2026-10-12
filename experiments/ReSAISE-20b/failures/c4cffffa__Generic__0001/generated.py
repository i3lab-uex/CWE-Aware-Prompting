import urllib.parse

# Example set of allowed domains – in real code this would be imported or defined elsewhere
ALLOWED_RETURN_DOMAINS = {"example.com", "trustedpartner.org"}

def build_sso_redirect_link(sso_service_url: str, user_identifier: str,
                            redirect_back_url: str) -> str:
    """
    Construct an SSO redirect URL that points to the third‑party service and
    includes the user identifier and a return URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_back_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        Fully formed URL that the client can be redirected to.

    Raises
    ------
    ValueError
        If ``redirect_back_url`` is not from an allowed domain.
    """
    # Validate the return URL's domain
    parsed_back = urllib.parse.urlparse(redirect_back_url)
    # Extract hostname without port
    host = parsed_back.hostname or ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Build the query parameters
    params = {
        "user_id": user_identifier,
        "return_url": redirect_back_url,
    }
    encoded_params = urllib.parse.urlencode(params)

    # Parse the SSO service URL to handle existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    # Merge existing query with new parameters
    if parsed_sso.query:
        new_query = f"{parsed_sso.query}&{encoded_params}"
    else:
        new_query = encoded_params

    # Reconstruct the full URL
    sso_redirect = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        new_query,
        parsed_sso.fragment
    ))

    return sso_redirect

# Example usage:
if __name__ == "__main__":
    try:
        url = build_sso_redirect_link(
            "https://sso.example.com/auth",
            user_identifier="user-12345",
            redirect_back_url="https://example.com/welcome"
        )
        print(url)
    except ValueError as e:
        print(f"Invalid URL: {e}")