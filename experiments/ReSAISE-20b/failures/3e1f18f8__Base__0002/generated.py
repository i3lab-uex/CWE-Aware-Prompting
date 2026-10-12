import urllib.parse

# Set of domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "myapp.local",
}

def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO service (e.g. "https://sso.example.com/auth").
    user_identifier : str
        The unique identifier for the user.
    redirect_uri : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user to the SSO service.

    Raises
    ------
    ValueError
        If ``redirect_uri`` resolves to a domain that is not in
        :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect_uri to inspect its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)

    # Reject absolute URLs that point to disallowed domains
    if parsed_redirect.scheme in ("http", "https"):
        domain = parsed_redirect.hostname or ""
        # Normalize to lowercase for comparison
        if domain.lower() not in ALLOWED_RETURN_DOMAINS:
            raise ValueError(
                f"Return URL domain '{domain}' is not allowed for redirection."
            )
        # Keep the full redirect_uri as provided
        safe_redirect = urllib.parse.urlunparse(parsed_redirect)
    else:
        # For relative URLs, we simply encode them
        safe_redirect = urllib.parse.quote(redirect_uri, safe="/")

    # Build the query parameters for the SSO request
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": safe_redirect,
    }

    # Parse the base auth endpoint to combine paths correctly
    parsed_auth = urllib.parse.urlparse(auth_service_endpoint)
    # Ensure the path ends with a slash to avoid accidental merging
    auth_path = parsed_auth.path.rstrip("/") + "/sso"

    # Assemble the final URL
    sso_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        auth_path,
        "",  # params
        urllib.parse.urlencode(query_params),
        "",  # fragment
    )
    return urllib.parse.urlunparse(sso_url_parts)