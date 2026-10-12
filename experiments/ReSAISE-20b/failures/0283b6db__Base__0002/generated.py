import urllib.parse

# Set of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
}

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base SSO service endpoint.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to which the user should be redirected after SSO.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If `return_url` does not belong to an allowed domain or is malformed.
    """
    # Parse the return URL
    parsed_return = urllib.parse.urlparse(return_url)

    # Basic validation: scheme must be http or https
    if parsed_return.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_return.scheme}")

    # Extract the hostname (domain) and normalize it
    domain = parsed_return.hostname
    if not domain:
        raise ValueError("Return URL must contain a valid hostname")

    # Reject subdomains that are not explicitly allowed
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed")

    # Reconstruct the return URL to ensure it is absolute and safe
    safe_return_url = urllib.parse.urlunparse(parsed_return)

    # Build query parameters for the SSO endpoint
    query_params = {
        "user_id": user_id,
        "return_url": safe_return_url,
    }
    query_string = urllib.parse.urlencode(query_params)

    # Construct the final redirect URL
    parsed_sso = urllib.parse.urlparse(sso_endpoint)
    # Preserve existing query parameters on the SSO endpoint
    sso_query = urllib.parse.parse_qs(parsed_sso.query)
    sso_query.update(query_params)
    final_query = urllib.parse.urlencode(sso_query, doseq=True)

    # Build the final URL
    redirect_parts = parsed_sso._replace(query=final_query)
    redirect_url = urllib.parse.urlunparse(redirect_parts)

    return redirect_url