import urllib.parse

# Domains that are allowed to receive the SSO redirect.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # Add more domains as needed
}


def create_sso_redirect_url(login_endpoint: str, account_id: str, callback_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO provider.
    account_id : str
        Unique identifier for the user that will be sent to the SSO provider.
    callback_url : str
        URL where the user should be redirected after successful authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If ``callback_url`` does not belong to one of the allowed domains.
    """
    # Validate that callback_url is a full URL
    parsed_callback = urllib.parse.urlparse(callback_url)
    if not parsed_callback.scheme or not parsed_callback.netloc:
        raise ValueError("callback_url must be a fully-qualified URL")

    # Normalize the domain (lowercase, strip port)
    domain = parsed_callback.hostname.lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Prepare query parameters
    params = {
        "account_id": account_id,
        "return_url": callback_url,
    }

    # Parse the login endpoint to preserve any existing query parameters
    parsed_login = urllib.parse.urlparse(login_endpoint)
    existing_params = dict(urllib.parse.parse_qsl(parsed_login.query))
    # Merge parameters, new ones override existing if conflict
    merged_params = {**existing_params, **params}

    # Rebuild the login URL with updated query string
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    final_url = parsed_login._replace(query=new_query).geturl()

    return final_url