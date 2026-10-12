import urllib.parse

# Example set of allowed domains – replace with your own.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a full SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO provider.
    uid : str
        User identifier to be sent to the provider.
    redirect_url : str
        URL where the user should be returned after authentication.

    Returns
    -------
    str
        The complete redirect URL that can be used in an HTTP redirect.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that the redirect URL is absolute and has a host
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Extract the hostname for domain validation
    hostname = parsed_redirect.hostname.lower()
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain '{hostname}' is not allowed. Allowed domains: "
            f"{', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Encode query parameters safely
    params = {
        "uid": uid,
        "redirect_uri": redirect_url,  # provider expects this param
    }
    query = urllib.parse.urlencode(params, safe="/:")

    # Combine the auth endpoint with query string
    # Ensure that auth_endpoint does not already contain a query
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if parsed_auth.query:
        # Append new params to existing query
        new_query = f"{parsed_auth.query}&{query}"
    else:
        new_query = query

    redirect_parts = parsed_auth._replace(query=new_query)
    return urllib.parse.urlunparse(redirect_parts)

# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.provider.com/auth"
    user_id = "user-12345"
    return_to = "https://example.com/welcome?foo=bar"

    try:
        url = build_sso_redirect(endpoint, user_id, return_to)
        print("Redirect URL:", url)
    except ValueError as exc:
        print("Error:", exc)