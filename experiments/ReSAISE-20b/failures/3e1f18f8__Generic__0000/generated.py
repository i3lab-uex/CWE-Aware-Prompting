import urllib.parse

# Set of allowed domains for the redirect URI
ALLOWED_RETURN_DOMAINS = {"example.com", "auth.example.org"}

def construct_sso_redirect(auth_service_endpoint: str,
                           user_identifier: str,
                           redirect_uri: str) -> str:
    """
    Build a complete SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO service endpoint.
    user_identifier : str
        Unique identifier for the user to be authenticated.
    redirect_uri : str
        URL where the user should be sent after authentication.

    Returns
    -------
    str
        Fully constructed redirect URL containing the user ID and
        percent‑encoded return URI as query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect_uri to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect_uri: missing scheme or netloc")

    # Extract the domain (netloc) and compare against allowed set
    # Normalize by removing port if present
    domain = parsed_redirect.netloc.split(':')[0]
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_uri
    }

    # Ensure the base endpoint has no trailing slash that could interfere with urljoin
    endpoint = auth_service_endpoint.rstrip('/')

    # Construct the final URL
    full_url = f"{endpoint}?{urllib.parse.urlencode(query_params, safe=':/?#[]@!$&'()*+,;=')}"
    return full_url