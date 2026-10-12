import urllib.parse

# Domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more trusted domains here
}

def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service endpoint.
    account_id : str
        Unique identifier for the user.
    callback_url : str
        URL to redirect to after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `callback_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the callback URL to extract its domain.
    parsed_cb = urllib.parse.urlparse(callback_url)
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError("callback_url must be a valid absolute URL")

    # Normalize the domain (remove port if present).
    domain = parsed_cb.hostname
    if domain is None:
        raise ValueError("callback_url must contain a hostname")

    # Ensure the domain is allowed.
    if domain.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Domain '{domain}' is not allowed for return URLs")

    # Build the query parameters safely.
    query_params = {
        "account_id": account_id,
        "return": callback_url,  # This will be percent‑encoded by urlencode
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Assemble the final redirect URL.
    parsed_login = urllib.parse.urlparse(login_endpoint)
    if not parsed_login.scheme or not parsed_login.netloc:
        raise ValueError("login_endpoint must be a valid absolute URL")

    # Preserve any existing query parameters on the login endpoint.
    existing_query = parsed_login.query
    combined_query = urllib.parse.urlencode(
        urllib.parse.parse_qsl(existing_query) + list(query_params.items()),
        doseq=True,
    )

    redirect_parts = (
        parsed_login.scheme,
        parsed_login.netloc,
        parsed_login.path,
        parsed_login.params,
        combined_query,
        parsed_login.fragment,
    )
    return urllib.parse.urlunparse(redirect_parts)