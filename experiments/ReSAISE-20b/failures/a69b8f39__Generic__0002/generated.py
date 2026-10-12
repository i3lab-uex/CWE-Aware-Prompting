import urllib.parse

# Domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trustedsite.net",
}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a Single Sign-On redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        The complete SSO redirect URL with encoded parameters.

    Raises
    ------
    ValueError
        If the domain of ``back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the back_url to ensure it contains a scheme and netloc.
    parsed_back = urllib.parse.urlparse(back_url)
    if not (parsed_back.scheme and parsed_back.netloc):
        raise ValueError(f"Return URL must be absolute: {back_url!r}")

    # Validate the domain.
    domain = parsed_back.hostname
    if not domain or domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Parse the SSO service URL to preserve existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_service)
    sso_query = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))

    # Add or override parameters for user_ref and back_url.
    sso_query["user"] = user_ref
    # Encode the return URL so it is safe as a query value.
    sso_query["return_url"] = back_url

    # Reconstruct the SSO URL with updated query string.
    new_query = urllib.parse.urlencode(sso_query, doseq=True)
    sso_redirect = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return sso_redirect