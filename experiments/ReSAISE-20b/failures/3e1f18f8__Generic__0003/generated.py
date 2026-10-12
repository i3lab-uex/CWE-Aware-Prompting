import urllib.parse

# Domains that are allowed as return URLs.  Add or remove domains as needed.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "localhost",
}

def construct_sso_redirect(auth_service_endpoint: str,
                           user_identifier: str,
                           redirect_uri: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        Base URL of the SSO service.
    user_identifier : str
        Unique identifier for the user (e.g., a UUID or login name).
    redirect_uri : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect_uri to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect_uri: {redirect_uri!r}")

    # Normalize the hostname (lowercase) and strip port if present
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain {host!r} not allowed. Allowed domains: "
            f"{', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build the query parameters, ensuring they are properly encoded
    params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_uri,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=")

    # Ensure the base endpoint ends with a separator before adding query
    if urllib.parse.urlparse(auth_service_endpoint).query:
        # Endpoint already has a query; append with &
        separator = "&"
    else:
        separator = "?"

    return f"{auth_service_endpoint}{separator}{query_string}"