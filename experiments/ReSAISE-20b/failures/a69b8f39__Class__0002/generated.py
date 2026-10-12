import urllib.parse

# Domains that are allowed for the return URL.  Add any trusted domains here.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more domains as needed
}


def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    user_ref : str
        Unique identifier for the user.
    back_url : str
        Absolute URL to redirect to after authentication.

    Returns
    -------
    str
        Full SSO redirect URL with user and return parameters encoded.

    Raises
    ------
    ValueError
        If the domain of ``back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain (CWE-610 mitigation)
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("back_url must be an absolute URL with scheme and netloc")

    # Extract the host part (without port)
    host = parsed_back.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Parse the SSO service URL
    parsed_sso = urllib.parse.urlparse(sso_service)

    # Prepare query parameters, preserving any existing ones
    sso_query = urllib.parse.parse_qs(parsed_sso.query)
    # parse_qs returns lists; flatten for single values
    sso_query = {k: v[0] if isinstance(v, list) else v for k, v in sso_query.items()}

    # Add or override user_ref and back_url
    sso_query.update({
        "user_ref": user_ref,
        "back_url": back_url
    })

    # Reconstruct the SSO URL with updated query string
    new_query = urllib.parse.urlencode(sso_query, doseq=False)
    sso_redirect = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        new_query,
        parsed_sso.fragment
    ))

    return sso_redirect