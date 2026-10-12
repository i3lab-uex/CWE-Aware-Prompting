import urllib.parse

# Example set of allowed domains for return URLs.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base SSO service endpoint.
    user_id : str
        Unique identifier of the user.
    return_url : str
        URL to redirect back after successful SSO.

    Returns
    -------
    str
        A fully‑qualified SSO redirect URL with the required query parameters.

    Raises
    ------
    ValueError
        If `return_url` does not belong to an allowed domain.
    """
    # Parse the return URL to extract its domain
    parsed_return = urllib.parse.urlparse(return_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("return_url must be a valid absolute URL")

    # Extract the domain (host) and check against allowed domains
    host = parsed_return.hostname or ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Build the query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    query_string = urllib.parse.urlencode(params)

    # Ensure the base endpoint ends with a slash or has a path
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    if not parsed_endpoint.scheme or not parsed_endpoint.netloc:
        raise ValueError("sso_endpoint must be a valid absolute URL")

    # Combine the endpoint with the query string
    sso_url = urllib.parse.urlunparse(
        (
            parsed_endpoint.scheme,
            parsed_endpoint.netloc,
            parsed_endpoint.path or "",
            parsed_endpoint.params,
            query_string,
            parsed_endpoint.fragment,
        )
    )

    return sso_url