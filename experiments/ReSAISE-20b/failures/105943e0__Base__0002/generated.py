import urllib.parse

# Set of domains that are allowed to be used as return URLs.
ALLOWED_RETURN_DOMAINS = {"example.com", "auth.example.org"}

def create_sso_redirect_url(login_endpoint: str, account_id: str,
                            callback_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO provider.
    account_id : str
        The unique identifier for the user that will be sent to the SSO provider.
    callback_url : str
        The URL to which the user should be returned after successful authentication.

    Returns
    -------
    str
        A fully constructed redirect URL that includes the account ID and a
        percent‑encoded return URL.

    Raises
    ------
    ValueError
        If the callback_url is not a valid absolute URL or its domain is not in
        ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the callback URL to inspect its components
    parsed_cb = urllib.parse.urlparse(callback_url)

    # Ensure the callback URL has a scheme and netloc (i.e., it is absolute)
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError("callback_url must be an absolute URL")

    # Validate the scheme (only http/https are allowed)
    if parsed_cb.scheme.lower() not in {"http", "https"}:
        raise ValueError("callback_url must use http or https scheme")

    # Validate the domain against the whitelist
    domain = parsed_cb.hostname.lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build the query parameters for the SSO endpoint
    query_params = {
        "account_id": account_id,
        "return_url": callback_url,  # will be percent‑encoded by urlencode
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Assemble the final redirect URL
    parsed_login = urllib.parse.urlparse(login_endpoint)
    if not parsed_login.scheme or not parsed_login.netloc:
        raise ValueError("login_endpoint must be an absolute URL")

    # Preserve existing query parameters on the login endpoint
    existing_query = parsed_login.query
    if existing_query:
        combined_query = f"{existing_query}&{encoded_query}"
    else:
        combined_query = encoded_query

    final_url_parts = parsed_login._replace(query=combined_query)
    return urllib.parse.urlunparse(final_url_parts)