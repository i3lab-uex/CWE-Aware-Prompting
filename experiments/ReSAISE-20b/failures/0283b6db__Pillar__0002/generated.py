import urllib.parse

# Domains that are allowed for the return URL.  In a real application these would
# be read from configuration or environment variables.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Build an SSO redirect URL that includes the user ID and a safe return URL.

    Parameters
    ----------
    sso_endpoint : str
        The base endpoint of the SSO provider.
    user_id : str
        Unique identifier for the authenticated user.
    return_url : str
        URL to redirect back after authentication. Must belong to an allowed domain.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If `return_url` is not a valid URL or its domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the return URL to validate it and extract its domain
    parsed_return = urllib.parse.urlparse(return_url)
    if not (parsed_return.scheme and parsed_return.netloc):
        raise ValueError("return_url must be a fully-qualified URL")

    # Normalise the domain for comparison
    return_domain = parsed_return.hostname.lower()
    if return_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"return_url domain '{return_domain}' is not allowed")

    # Build query parameters.  `return_url` is URL‑encoded to preserve its structure.
    query_params = {
        "user_id": user_id,
        "return_url": return_url
    }
    encoded_query = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    # Construct the final URL.  `urljoin` handles trailing slashes correctly.
    base = urllib.parse.urljoin(sso_endpoint, "?")
    sso_redirect_url = f"{base}{encoded_query}"
    return sso_redirect_url