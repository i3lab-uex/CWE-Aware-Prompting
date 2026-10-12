import urllib.parse

# Example set of allowed domains; replace with your actual list.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org", "trusted.io"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the user.
    redirect_back_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully constructed redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate that the redirect_back_url domain is allowed
    parsed_redirect = urllib.parse.urlparse(redirect_back_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_back_url must be a valid absolute URL")

    # Extract the hostname without port
    host = parsed_redirect.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Prepare query parameters
    params = {
        "user_id": user_identifier,
        "redirect_back_url": redirect_back_url
    }

    # Encode query string safely
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)

    # Build final URL
    base = urllib.parse.urlparse(sso_service_url)
    if not base.scheme or not base.netloc:
        raise ValueError("sso_service_url must be a valid absolute URL")

    # Ensure no trailing slash issues
    path = base.path.rstrip("/")
    final_url = urllib.parse.urlunparse(
        (
            base.scheme,
            base.netloc,
            path + "/login",  # assume the endpoint is /login
            "",              # params
            encoded_params,
            ""               # fragment
        )
    )

    return final_url

# Example usage:
if __name__ == "__main__":
    try:
        url = build_sso_redirect_link(
            "https://sso.example.com/auth",
            "user-12345",
            "https://myapp.org/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")