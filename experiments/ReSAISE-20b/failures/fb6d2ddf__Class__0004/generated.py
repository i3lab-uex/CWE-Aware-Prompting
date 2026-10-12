import urllib.parse

# Whitelist of domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # add more trusted domains here
}

def _is_allowed_domain(url: str) -> bool:
    """
    Verify that the domain of `url` is in ALLOWED_RETURN_DOMAINS.
    The check is performed on the hostname part of the URL.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    # Normalize hostname (lowercase, strip trailing dot)
    host = parsed.hostname.lower().rstrip(".")
    # Support subdomains of allowed domains if needed:
    return any(host == domain or host.endswith("." + domain) for domain in ALLOWED_RETURN_DOMAINS)

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that includes the user ID and the return URL.
    
    Parameters
    ----------
    auth_endpoint : str
        Base SSO endpoint URL (e.g., "https://sso.example.com/auth").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If `redirect_url` is not a valid absolute URL or its domain is not in
        ALLOWED_RETURN_DOMAINS.
    """
    # Validate redirect_url domain
    if not _is_allowed_domain(redirect_url):
        raise ValueError(f"Redirect URL domain is not allowed: {redirect_url}")

    # Parse the auth endpoint to manipulate its query parameters
    parsed_endpoint = urllib.parse.urlparse(auth_endpoint)
    # Extract existing query params and convert to dict
    query_params = urllib.parse.parse_qs(parsed_endpoint.query, keep_blank_values=True)

    # Add/override uid and redirect_url parameters
    query_params["uid"] = [uid]
    query_params["redirect_uri"] = [redirect_url]

    # Reconstruct the query string with proper encoding
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Build the final URL
    new_url = urllib.parse.urlunparse((
        parsed_endpoint.scheme,
        parsed_endpoint.netloc,
        parsed_endpoint.path,
        parsed_endpoint.params,
        encoded_query,
        parsed_endpoint.fragment
    ))
    return new_url