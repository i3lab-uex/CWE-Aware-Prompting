import urllib.parse

# Set of domains that are allowed as callback URLs.
ALLOWED_RETURN_DOMAINS = {"example.com", "trustedpartner.org"}

def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Build a redirect URL for SSO authentication.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service endpoint.
    account_id : str
        Unique identifier for the user/account.
    callback_url : str
        The URL to return to after authentication.

    Returns
    -------
    str
        A fully formed redirect URL containing the SSO endpoint, user ID,
        and encoded return URL.

    Raises
    ------
    ValueError
        If the domain of ``callback_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the callback URL to validate its domain
    parsed_cb = urllib.parse.urlparse(callback_url)
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError(f"Invalid callback URL: {callback_url!r}")

    # Extract the hostname (domain) and normalize it
    host = parsed_cb.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Callback domain {host!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Build query parameters
    params = {
        "account_id": account_id,
        "return_url": callback_url,  # will be quoted in the query string
    }

    # Encode parameters ensuring safe URL construction
    query_string = urllib.parse.urlencode(params, doseq=True)

    # Construct the final redirect URL
    # Preserve any existing query or fragment in login_endpoint
    base = urllib.parse.urlparse(login_endpoint)
    new_query = urllib.parse.parse_qs(base.query)
    # Merge with our params
    merged_query = {**new_query, **params}
    final_query = urllib.parse.urlencode(merged_query, doseq=True)

    redirect_parts = (
        base.scheme,
        base.netloc,
        base.path,
        base.params,
        final_query,
        base.fragment,
    )
    return urllib.parse.urlunparse(redirect_parts)