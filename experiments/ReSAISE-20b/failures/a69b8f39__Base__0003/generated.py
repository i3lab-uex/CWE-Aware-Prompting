import urllib.parse

# Domains that are allowed to be used as a return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    # add any additional trusted domains here
}


def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to redirect back after SSO. Must belong to an allowed domain.

    Returns
    -------
    str
        Full URL that can be used for redirecting the user to the SSO service.

    Raises
    ------
    ValueError
        If ``back_url`` is not a valid absolute URL or its domain is not in
        :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL and its domain
    parsed_back = urllib.parse.urlparse(back_url)
    if not (parsed_back.scheme and parsed_back.netloc):
        raise ValueError("Return URL must be a fully-qualified absolute URL")

    host = parsed_back.hostname
    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Prepare query parameters to be added to the SSO service URL
    params = {
        "user_ref": user_ref,
        "back_url": back_url,  # The full URL will be percent‑encoded by urlencode
    }

    # Parse the SSO service base URL and merge existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_service)
    existing_qs = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    merged_qs = {**existing_qs, **params}

    # Reconstruct the SSO URL with the merged query string
    new_query = urllib.parse.urlencode(merged_qs, doseq=True)
    new_sso_url = parsed_sso._replace(query=new_query)

    return urllib.parse.urlunparse(new_sso_url)