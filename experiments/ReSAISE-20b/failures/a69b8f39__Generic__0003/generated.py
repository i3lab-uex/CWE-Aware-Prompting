import urllib.parse

# Domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        The base URL of the SSO service.
    user_ref : str
        Unique identifier for the user to be passed to the SSO service.
    back_url : str
        URL to which the user should be redirected after successful SSO.

    Returns
    -------
    str
        The fully‑qualified redirect URL ready to be sent to the user.

    Raises
    ------
    ValueError
        If the domain of ``back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # 1. Validate the return URL's domain.
    parsed_back = urllib.parse.urlparse(back_url)
    host = parsed_back.hostname
    if not host:
        raise ValueError("Return URL must contain a valid hostname")

    # Allow subdomains of the allowed domains as well.
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # 2. Build query parameters to append.
    params = {
        "user_ref": user_ref,
        "back_url": back_url,          # the SSO service should be able to parse this
    }

    # 3. Parse the SSO service URL and merge any existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_service)
    # Existing query params
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query))
    # Merge with new params (new ones override existing)
    merged_params = {**existing_params, **params}

    # 4. Construct the final URL.
    new_query = urllib.parse.urlencode(merged_params)
    final_url_parts = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(final_url_parts)