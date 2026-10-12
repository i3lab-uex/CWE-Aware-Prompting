import urllib.parse

# Example whitelist of allowed return domains.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org", "myapp.local"}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base SSO endpoint URL (may already contain query parameters).
    user_identifier : str
        Unique identifier for the user.
    redirect_link : str
        Destination URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully-formed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_link` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect_link domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    hostname = parsed_redirect.hostname
    if not hostname:
        raise ValueError("Redirect link must contain a valid hostname")

    # Normalize domain for comparison
    if hostname.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for redirects")

    # Parse the base SSO URI to preserve existing components
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Merge existing query parameters with new ones
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    new_params = {
        "user_id": user_identifier,
        "return_url": redirect_link
    }
    # New params should override existing ones if there's a conflict
    merged_params = {**existing_params, **new_params}
    encoded_query = urllib.parse.urlencode(merged_params)

    # Reconstruct the full URL
    sso_redirect = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        encoded_query,
        parsed_sso.fragment
    ))

    return sso_redirect

# Example usage (for testing purposes only)
if __name__ == "__main__":
    base_sso = "https://sso.example.com/auth?locale=en"
    user_id = "user-12345"
    return_url = "https://example.com/welcome?ref=signup"

    try:
        url = construct_sso_redirect(base_sso, user_id, return_url)
        print(url)
    except ValueError as e:
        print(f"Invalid redirect URL: {e}")