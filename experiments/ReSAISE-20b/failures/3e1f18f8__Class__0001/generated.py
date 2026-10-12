import urllib.parse

# Example set of allowed return domains.
# In real code this should be imported from a secure configuration module.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def construct_sso_redirect(auth_service_endpoint: str,
                           user_identifier: str,
                           redirect_uri: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO service.
    user_identifier : str
        Unique identifier for the authenticated user.
    redirect_uri : str
        URL to return to after authentication.

    Returns
    -------
    str
        A fully-formed redirect URL containing the SSO endpoint,
        user identifier, and encoded return URI.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the return URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a full absolute URL")

    # Extract hostname (e.g., 'sub.example.com')
    host = parsed_redirect.hostname
    if not host:
        raise ValueError("redirect_uri must contain a hostname")

    # Ensure the domain is allowed. We allow subdomains of any approved domain.
    if not any(host == d or host.endswith("." + d) for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"Domain '{host}' is not allowed for redirect_uri")

    # Parse the SSO endpoint and preserve existing query parameters
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)
    existing_params = dict(urllib.parse.parse_qsl(parsed_endpoint.query))

    # Add/override the SSO-specific parameters
    existing_params.update({
        "user": user_identifier,
        "redirect_uri": redirect_uri
    })

    # Reconstruct the URL with updated query string
    new_query = urllib.parse.urlencode(existing_params, doseq=True)
    rebuilt_endpoint = parsed_endpoint._replace(query=new_query)

    return urllib.parse.urlunparse(rebuilt_endpoint)