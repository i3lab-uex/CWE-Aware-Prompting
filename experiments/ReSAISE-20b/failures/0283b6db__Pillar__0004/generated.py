import urllib.parse

# Domains that are allowed to be used as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more allowed domains here
}

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to redirect back after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the return_url's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse and validate the return URL
    parsed_return = urllib.parse.urlparse(return_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("Return URL must be a fully-qualified absolute URL")

    # Normalize domain (lowercase, strip port)
    host = parsed_return.hostname
    if not host:
        raise ValueError("Return URL must contain a valid hostname")

    # Check against allowed domains
    if host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Build query parameters for the SSO endpoint
    sso_params = {
        "user_id": user_id,
        "return_url": return_url,  # Preserve the full URL
    }

    # Encode parameters safely
    encoded_params = urllib.parse.urlencode(sso_params, quote_via=urllib.parse.quote)

    # Construct the final SSO redirect URL
    # Ensure we preserve any existing query parameters on the endpoint
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    if parsed_endpoint.query:
        # Append to existing query
        final_query = f"{parsed_endpoint.query}&{encoded_params}"
    else:
        final_query = encoded_params

    # Rebuild the full URL
    final_url_parts = parsed_endpoint._replace(query=final_query)
    return urllib.parse.urlunparse(final_url_parts)


# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.example.com/login"
    uid = "user-12345"
    ret_url = "https://example.com/dashboard"

    try:
        redirect_url = generate_sso_redirect(endpoint, uid, ret_url)
        print("Redirect URL:", redirect_url)
    except ValueError as e:
        print("Error generating SSO redirect:", e)