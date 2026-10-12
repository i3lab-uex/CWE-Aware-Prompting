import urllib.parse

# Example whitelist – in real code this would be defined elsewhere
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted.partner.net",
}

def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Build an SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint.
    user_identifier : str
        Unique identifier for the user to be authenticated.
    redirect_link : str
        URL that the client should be returned to after authentication.

    Returns
    -------
    str
        Fully‑qualified redirect URL ready for the client to visit.

    Raises
    ------
    ValueError
        If the domain of `redirect_link` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    if not parsed_redirect.netloc:
        raise ValueError("Redirect link must be a full URL with a domain")

    # Extract the hostname (domain) for whitelist comparison
    host = parsed_redirect.hostname or ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{host}' is not allowed")

    # Parse the SSO endpoint to preserve any existing components
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Merge existing query parameters with new ones
    qs = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # Ensure parameters are single-valued
    qs.update({
        "user_id": [user_identifier],
        "redirect_uri": [redirect_link]
    })

    # Reconstruct the query string
    new_query = urllib.parse.urlencode(qs, doseq=True)

    # Build the final URL
    new_sso = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(new_sso)

# Example usage
if __name__ == "__main__":
    sso = "https://sso.provider.com/auth"
    user_id = "alice123"
    return_url = "https://app.example.org/dashboard"

    print(construct_sso_redirect(sso, user_id, return_url))