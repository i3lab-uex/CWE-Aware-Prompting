import urllib.parse

# Domains that are allowed to receive the user after SSO.
ALLOWED_RETURN_DOMAINS = {"example.com", "app.example.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the third‑party SSO provider.
    user_identifier : str
        Unique identifier for the user (e.g., username or UUID).
    redirect_back_url : str
        URL to return the user to after authentication.

    Returns
    -------
    str
        A fully formed SSO redirect URL containing the user identifier and a
        return parameter that is guaranteed to point only to an allowed domain.

    Raises
    ------
    ValueError
        If the `redirect_back_url` does not belong to an allowed domain.
    """
    # Parse the return URL and validate its domain
    parsed_back = urllib.parse.urlparse(redirect_back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("redirect_back_url must be a fully qualified URL")

    # Extract hostname (strip port if present)
    host = parsed_back.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{host}' is not in the list of allowed domains"
        )

    # Build query parameters for SSO
    sso_params = {
        "user_id": user_identifier,
        # Encode the return URL to avoid injection
        "return_to": redirect_back_url,
    }
    encoded_params = urllib.parse.urlencode(sso_params, quote_via=urllib.parse.quote)

    # Construct the final SSO redirect URL
    sso_parsed = urllib.parse.urlparse(sso_service_url)
    # Ensure the SSO URL has a scheme and netloc
    if not sso_parsed.scheme or not sso_parsed.netloc:
        raise ValueError("sso_service_url must be a fully qualified URL")

    # Append the query string to the SSO service path
    sso_path = urllib.parse.urljoin(sso_parsed.path + "/", "")
    final_url = urllib.parse.urlunparse((
        sso_parsed.scheme,
        sso_parsed.netloc,
        sso_path,
        "",  # params
        encoded_params,
        ""   # fragment
    ))
    return final_url