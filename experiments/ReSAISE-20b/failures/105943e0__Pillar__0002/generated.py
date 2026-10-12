import urllib.parse

# Allowed domains for the callback URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    "sso.mycompany.io",
}

def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO provider.
    account_id : str
        The unique identifier for the user.
    callback_url : str
        URL to return to after successful authentication.

    Returns
    -------
    str
        The full redirect URL including the user ID and callback URI.

    Raises
    ------
    ValueError
        If the domain of `callback_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the callback URL's domain
    parsed_callback = urllib.parse.urlparse(callback_url)
    if not parsed_callback.scheme or not parsed_callback.netloc:
        raise ValueError("Invalid callback URL: missing scheme or netloc")

    # Extract domain and check against allowed set
    domain = parsed_callback.netloc.split(":")[0]  # strip port if present
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Callback domain '{domain}' is not allowed")

    # Build the query parameters safely
    query_params = {
        "user": account_id,
        "redirect_uri": callback_url,
    }
    encoded_query = urllib.parse.urlencode(query_params, safe=":/?#[]@!$&'()*+,;=")

    # Ensure the login endpoint ends with a '?' or '&'
    if urllib.parse.urlparse(login_endpoint).query:
        separator = "&"
    else:
        separator = "?"

    return f"{login_endpoint}{separator}{encoded_query}"