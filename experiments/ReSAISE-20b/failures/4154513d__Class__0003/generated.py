import urllib.parse

# Domains that are allowed to receive the SSO redirect.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO service endpoint.
    uid : str
        Unique identifier for the user to be authenticated.
    redirect_url : str
        Destination URL after successful authentication.

    Returns
    -------
    str
        The fully formed redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect URL's domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a full URL with scheme and domain")

    # Extract the hostname (e.g., example.com) for validation
    host = parsed_redirect.hostname or ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{host}' is not allowed")

    # Build the query parameters
    params = {
        "uid": uid,
        "redirect_url": redirect_url,  # will be percent‑encoded by urlencode
    }

    # Parse the auth endpoint to handle existing query params
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Merge any existing query parameters with our new ones
    existing_params = urllib.parse.parse_qs(parsed_auth.query)
    # parse_qs returns values as lists; flatten them for simplicity
    flattened_existing = {k: v[0] if len(v) == 1 else v for k, v in existing_params.items()}
    merged_params = {**flattened_existing, **params}

    # Reconstruct the auth URL with updated query string
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    auth_url_parts = parsed_auth._replace(query=new_query)
    return urllib.parse.urlunparse(auth_url_parts)

# Example usage:
if __name__ == "__main__":
    try:
        url = build_sso_redirect(
            auth_endpoint="https://sso.example.com/auth",
            uid="user123",
            redirect_url="https://app.example.com/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")