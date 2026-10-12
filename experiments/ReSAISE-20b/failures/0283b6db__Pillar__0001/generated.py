import urllib.parse

# Domains that are allowed to be used as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
    "trustedpartner.net",
}

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service (e.g., "https://sso.example.com/auth").
    user_id : str
        The unique identifier of the user.
    return_url : str
        The URL to redirect back after successful SSO.

    Returns
    -------
    str
        A fully constructed SSO redirect URL containing the user ID and return URL as query parameters.

    Raises
    ------
    ValueError
        If the return_url does not belong to an allowed domain.
    """
    # Parse the return URL and verify its domain
    parsed_return = urllib.parse.urlparse(return_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("return_url must be a valid absolute URL")

    # Extract the hostname for domain validation
    host = parsed_return.hostname
    if host is None or not any(host == allowed or host.endswith("." + allowed) for allowed in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"return_url domain '{host}' is not allowed")

    # Build the query parameters
    query_params = {
        "user_id": user_id,
        "return_url": return_url,  # encode later
    }

    # Encode the parameters safely
    encoded_query = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

    # Combine with the SSO endpoint
    if urllib.parse.urlparse(sso_endpoint).scheme == "":
        raise ValueError("sso_endpoint must be an absolute URL with a scheme")

    # Ensure there's no trailing slash that would interfere
    sso_base = sso_endpoint.rstrip("/")

    # Final redirect URL
    final_url = f"{sso_base}?{encoded_query}"
    return final_url