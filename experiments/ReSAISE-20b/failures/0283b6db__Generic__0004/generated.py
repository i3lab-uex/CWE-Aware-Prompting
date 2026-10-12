import urllib.parse

# Example allowed domains – replace with actual values in production.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def _is_allowed_return_url(url: str) -> bool:
    """
    Check if the provided URL belongs to an allowed domain.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        # Ensure the URL is absolute and has a scheme.
        if not parsed.scheme or not parsed.netloc:
            return False
        domain = parsed.hostname.lower()
        # Strip 'www.' prefix for comparison.
        if domain.startswith("www."):
            domain = domain[4:]
        return domain in ALLOWED_RETURN_DOMAINS
    except Exception:
        return False

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base SSO service endpoint.
    user_id : str
        The user's unique identifier.
    return_url : str
        URL to redirect back after authentication.

    Returns
    -------
    str
        The complete SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If `return_url` is not from an allowed domain.
    """
    if not _is_allowed_return_url(return_url):
        raise ValueError("Return URL domain is not allowed")

    # Parse the SSO endpoint to preserve existing query parameters.
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    # Merge existing query params with new ones.
    query_params = dict(urllib.parse.parse_qsl(parsed_endpoint.query))
    # Add or overwrite user_id and return_url parameters.
    query_params.update({
        "user_id": user_id,
        "return_url": return_url
    })
    # Reconstruct the URL.
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    redirect_parts = parsed_endpoint._replace(query=new_query)
    return urllib.parse.urlunparse(redirect_parts)

# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.example.com/login"
    uid = "user12345"
    ret_url = "https://myapp.org/dashboard"

    try:
        redirect_url = generate_sso_redirect(endpoint, uid, ret_url)
        print("Redirect URL:", redirect_url)
    except ValueError as e:
        print("Error:", e)