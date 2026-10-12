import urllib.parse

# Set of domains that are permitted for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trusted-site.net",
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
        The base URL of the SSO service.
    user_identifier : str
        Unique identifier for the user.
    redirect_uri : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        A fully formed redirect URL that can be used to initiate SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URI to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a valid absolute URL")

    # Normalize the domain (lowercase and strip port if present)
    netloc = parsed_redirect.netloc.split(":")[0].lower()
    if netloc not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"redirect_uri domain '{netloc}' is not allowed. "
            "Allowed domains: "
            f"{', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters
    params = {
        "user_id": user_identifier,
        "return_url": redirect_uri,
    }

    # Construct the final URL
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)

    # Combine the endpoint with new query string
    final_parts = (
        parsed_endpoint.scheme,
        parsed_endpoint.netloc,
        parsed_endpoint.path or "",
        parsed_endpoint.params,
        query_string,
        parsed_endpoint.fragment,
    )
    return urllib.parse.urlunparse(final_parts)