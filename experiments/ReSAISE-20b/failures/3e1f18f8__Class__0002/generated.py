import urllib.parse

# Example set of allowed return domains; replace with actual values in production.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trusted-site.net",
}


def construct_sso_redirect(auth_service_endpoint: str,
                           user_identifier: str,
                           redirect_uri: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO provider.
    user_identifier : str
        Unique identifier for the user to be authenticated.
    redirect_uri : str
        Absolute URL where the user should return after authentication.

    Returns
    -------
    str
        Fully constructed redirect URL ready to be sent to the client.

    Raises
    ------
    ValueError
        If ``redirect_uri`` points to a domain not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that redirect_uri is a well‑formed absolute URL
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not (parsed_redirect.scheme and parsed_redirect.netloc):
        raise ValueError("redirect_uri must be an absolute URL")

    # Extract the hostname and compare against allowed domains
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain '{host}' is not allowed for SSO redirects."
        )

    # Prepare query parameters, ensuring proper URL encoding
    params = {
        "user": user_identifier,
        "redirect_uri": redirect_uri,  # encode later in the final URL
    }

    # Encode parameters. Use safe='' to force encoding of all special chars.
    query_string = urllib.parse.urlencode(params, doseq=True, safe="")

    # Build the final URL
    if urllib.parse.urlparse(auth_service_endpoint).query:
        separator = "&"
    else:
        separator = "?"
    return f"{auth_service_endpoint}{separator}{query_string}"