import urllib.parse

# Domains that are considered safe for the callback URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "auth.example.org"}

def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service.
    account_id : str
        Unique identifier for the user/account.
    callback_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        The fully formed redirect URL.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the callback URL to extract its domain
    parsed_cb = urllib.parse.urlparse(callback_url)
    host = parsed_cb.hostname

    if not host or host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Unallowed callback domain: {host}")

    # Build query parameters
    params = {
        "account_id": account_id,
        "return_url": callback_url
    }

    # Ensure the login endpoint is parsed correctly
    parsed_le = urllib.parse.urlparse(login_endpoint)
    # Merge existing query parameters if any
    existing_query = dict(urllib.parse.parse_qsl(parsed_le.query))
    merged_params = {**existing_query, **params}

    # Reconstruct the login URL with updated query
    new_le = parsed_le._replace(query=urllib.parse.urlencode(merged_params))
    return urllib.parse.urlunparse(new_le)