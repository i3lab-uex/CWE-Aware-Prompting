import urllib.parse

# Example set of allowed return domains; replace with your own.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trustedsite.net"
}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        A fully formed redirect URL containing the user ID and return URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect URL: missing scheme or host")

    # Extract the hostname (without port)
    hostname = parsed_redirect.hostname
    if not hostname or hostname.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Return URL domain '{hostname}' is not allowed")

    # Prepare query parameters, ensuring proper encoding
    query_params = {
        "uid": uid,
        # The redirect URL itself must be percent‑encoded
        "redirect_url": redirect_url
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Parse the base SSO URL to safely merge query parameters
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Merge existing query params if any
    sso_query = urllib.parse.parse_qs(parsed_sso.query)
    # Update with our parameters
    sso_query.update(query_params)

    # Rebuild the full URL
    new_sso_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        urllib.parse.urlencode(sso_query, doseq=True),
        parsed_sso.fragment
    ))

    return new_sso_url

# Example usage (commented out)
# if __name__ == "__main__":
#     url = create_sso_redirect_url(
#         "https://sso.example.com/login",
#         uid="user123",
#         redirect_url="https://example.com/welcome"
#     )
#     print(url)