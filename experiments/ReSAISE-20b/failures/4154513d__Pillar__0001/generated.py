import urllib.parse

# Set of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add additional trusted domains here.
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its components.
    parsed_redirect = urllib.parse.urlparse(redirect_url)

    # Ensure the URL has a scheme and netloc; otherwise, it is malformed.
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Redirect URL must be a valid absolute URL.")

    # Validate the domain against the allowed list.
    # ``parsed_redirect.netloc`` may contain port information; we strip it.
    domain = parsed_redirect.hostname
    if not domain or domain.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Redirect URL domain '{domain}' is not allowed.")

    # Build query parameters for the SSO request.
    params = {
        "uid": uid,
        # The redirect URI must be URL‑encoded to preserve any special characters.
        "redirect_uri": redirect_url,
    }

    # Construct the final SSO URL:
    #   1. Parse the base endpoint to preserve any existing query components.
    #   2. Append/merge our parameters.
    parsed_endpoint = urllib.parse.urlparse(auth_endpoint)
    # Merge existing query params with our new ones.
    existing_query = urllib.parse.parse_qs(parsed_endpoint.query)
    # ``parse_qs`` returns lists; convert to simple values for merging.
    merged_query = {k: v[0] if isinstance(v, list) else v for k, v in existing_query.items()}
    merged_query.update(params)

    # Rebuild the URL with updated query string.
    new_url_parts = parsed_endpoint._replace(query=urllib.parse.urlencode(merged_query))
    sso_redirect_url = urllib.parse.urlunparse(new_url_parts)

    return sso_redirect_url