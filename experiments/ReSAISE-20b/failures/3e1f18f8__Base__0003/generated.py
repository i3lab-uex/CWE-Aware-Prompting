import urllib.parse

# Allowed domains for the redirect URI.  In a real application this should be
# populated from configuration or environment variables.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "auth.mycompany.io"
}

def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO service (may already contain query parameters).
    user_identifier : str
        The unique identifier for the user to be authenticated.
    redirect_uri : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the redirect_uri is malformed or its domain is not in
        ALLOWED_RETURN_DOMAINS.
    """
    # Validate the redirect_uri
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not (parsed_redirect.scheme and parsed_redirect.netloc):
        raise ValueError("Invalid redirect_uri: must be a full URL with scheme and host")

    # Normalize the hostname (lowercase, strip port)
    hostname = parsed_redirect.hostname.lower()
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{hostname}' is not allowed")

    # Parse the auth service endpoint to preserve any existing query params
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)

    # Merge existing query parameters with the new ones
    existing_params = dict(urllib.parse.parse_qsl(parsed_endpoint.query, keep_blank_values=True))
    new_params = {
        "user": user_identifier,
        "redirect_uri": redirect_uri
    }
    merged_params = {**existing_params, **new_params}

    # Encode parameters and rebuild the URL
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    rebuilt_endpoint = parsed_endpoint._replace(query=new_query)

    return urllib.parse.urlunparse(rebuilt_endpoint)