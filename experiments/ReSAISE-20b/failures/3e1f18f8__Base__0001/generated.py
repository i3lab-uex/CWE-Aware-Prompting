import urllib.parse

# Set of domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trusted-domain.net",
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
        Base endpoint of the SSO provider.
    user_identifier : str
        Unique identifier for the authenticated user.
    redirect_uri : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully constructed redirect URL for the SSO flow.

    Raises
    ------
    ValueError
        If `redirect_uri` contains a domain not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the redirect URI and validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or parsed_redirect.scheme.lower() not in {"http", "https"}:
        raise ValueError("redirect_uri must use http or https scheme")

    # Extract the hostname; for IPv6 addresses, netloc may contain brackets
    host = parsed_redirect.hostname
    if not host:
        raise ValueError("redirect_uri must contain a valid hostname")

    # Reject any subdomains not explicitly allowed
    if host.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not allowed for redirect_uri")

    # Encode the redirect URI to ensure safe inclusion as a query parameter
    encoded_redirect = urllib.parse.quote(redirect_uri, safe="")

    # Build the query parameters
    params = {
        "user_id": user_identifier,
        "redirect_uri": encoded_redirect,
    }

    # Parse the SSO endpoint to merge any existing query components
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)
    existing_query = dict(urllib.parse.parse_qsl(parsed_endpoint.query, keep_blank_values=True))
    merged_query = {**existing_query, **params}
    query_string = urllib.parse.urlencode(merged_query)

    # Reconstruct the full URL
    final_url_parts = parsed_endpoint._replace(query=query_string)
    return urllib.parse.urlunparse(final_url_parts)

# Example usage
if __name__ == "__main__":
    try:
        url = construct_sso_redirect(
            "https://sso.example.com/auth",
            "user-12345",
            "https://example.com/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")