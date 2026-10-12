import urllib.parse

# Define the set of domains that are permitted for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    "trustedpartner.net"
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
        URL to which users should be returned after authentication.

    Returns
    -------
    str
        The complete redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the callback URL to validate its domain
    parsed_cb = urllib.parse.urlparse(callback_url)

    # Reject relative URLs to avoid open redirects
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError("Callback URL must be absolute and contain a valid domain.")

    # Extract the hostname for comparison
    host = parsed_cb.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{host}' is not allowed for callback URLs.")

    # Ensure the callback URL is properly encoded
    encoded_callback = urllib.parse.quote_plus(callback_url)

    # Build the query parameters for the SSO endpoint
    params = {
        "account_id": account_id,
        "return_url": callback_url  # Let the SSO service handle encoding
    }

    # Construct the full redirect URL
    # Parse the login endpoint to ensure it's a valid base URL
    parsed_login = urllib.parse.urlparse(login_endpoint)
    if not parsed_login.scheme or not parsed_login.netloc:
        raise ValueError("Login endpoint must be a valid absolute URL.")

    # Append query parameters to the login endpoint
    new_query = urllib.parse.urlencode(params, doseq=True)
    redirect_parts = parsed_login._replace(query=new_query)

    return urllib.parse.urlunparse(redirect_parts)