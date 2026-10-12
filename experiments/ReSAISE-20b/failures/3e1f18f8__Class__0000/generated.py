import urllib.parse

# Set of domains allowed for the redirect URI.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # add other domains as needed
}

def construct_sso_redirect(auth_service_endpoint: str,
                           user_identifier: str,
                           redirect_uri: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        Base URL of the SSO service (e.g. "https://sso.provider.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g. a GUID or username).
    redirect_uri : str
        The URL to return the user to after authentication.

    Returns
    -------
    str
        A fully constructed redirect URL that can be sent to the client.

    Raises
    ------
    ValueError
        If the domain of `redirect_uri` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URI to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a valid absolute URL")

    # Normalize the hostname (case‑insensitive for DNS).
    host = parsed_redirect.hostname.lower()

    # Verify that the hostname ends with one of the allowed domains.
    if not any(host == domain or host.endswith("." + domain) for domain in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"redirect_uri domain '{host}' is not allowed")

    # Construct query parameters.  Use `urllib.parse.quote_plus` for safe encoding.
    query_params = {
        "user": user_identifier,
        "redirect_uri": redirect_uri
    }
    encoded_params = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    # Combine the base endpoint with the encoded query string.
    # Ensure that we preserve any existing path or query in the endpoint.
    base = urllib.parse.urlparse(auth_service_endpoint)
    # Merge existing query parameters if any
    existing_params = urllib.parse.parse_qs(base.query)
    # Flatten to single values for simplicity
    existing_params = {k: v[0] if isinstance(v, list) else v for k, v in existing_params.items()}
    # Merge with new params; new ones override existing if duplicate
    all_params = {**existing_params, **query_params}
    final_query = urllib.parse.urlencode(all_params, quote_via=urllib.parse.quote)

    # Rebuild the full URL
    redirect_url = urllib.parse.urlunparse((
        base.scheme,
        base.netloc,
        base.path,
        base.params,
        final_query,
        base.fragment
    ))
    return redirect_url