import urllib.parse

# Set of domains that are allowed to be used as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
    # Add more allowed domains here
}


def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base SSO service endpoint.
    user_id : str
        The unique identifier of the user.
    return_url : str
        The URL to redirect back to after successful SSO.

    Returns
    -------
    str
        A fully-formed URL that the client can use to initiate SSO.

    Raises
    ------
    ValueError
        If the return URL's domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the return URL to inspect its components.
    parsed_return = urllib.parse.urlparse(return_url)

    # Ensure the URL is absolute and has a scheme.
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError(f"Return URL must be absolute: {return_url}")

    # Extract the domain and check against allowed domains.
    domain = parsed_return.hostname
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed.")

    # Prepare query parameters for the SSO endpoint.
    params = {
        "user_id": user_id,
        "return_url": return_url
    }

    # Build the final URL.
    query_string = urllib.parse.urlencode(params, safe=':/')
    # Use urljoin to correctly append the query string even if sso_endpoint has a path.
    final_url = urllib.parse.urljoin(sso_endpoint, '?' + query_string)

    return final_url