import urllib.parse

# Domains that are allowed to be used as the redirect URI.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trustedpartner.net"
}


def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        Base URL of the SSO provider (e.g. "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the authenticated user.
    redirect_uri : str
        The URL to which the provider should redirect after authentication.

    Returns
    -------
    str
        A fully‑qualified URL that can be sent to the user agent.

    Raises
    ------
    ValueError
        If ``redirect_uri`` points to a domain that is not in
        :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URI and validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a valid absolute URL")

    # Normalize the domain (lowercase) for comparison
    redirect_domain = parsed_redirect.hostname.lower()
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{redirect_domain}' is not allowed for redirect_uri")

    # Encode the redirect URI so it can safely be embedded as a query parameter
    encoded_redirect = urllib.parse.quote(redirect_uri, safe="")

    # Parse the base auth service endpoint to handle existing query parameters
    parsed_auth = urllib.parse.urlparse(auth_service_endpoint)

    # Build the new query string with existing parameters preserved
    original_query = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)
    # Flatten parse_qs result for easier manipulation
    query_params = {k: v[0] if len(v) == 1 else v for k, v in original_query.items()}

    # Add or override SSO specific parameters
    query_params["user"] = user_identifier
    query_params["redirect_uri"] = encoded_redirect

    # Reconstruct the final URL
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    final_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        new_query,
        parsed_auth.fragment
    )
    return urllib.parse.urlunparse(final_url_parts)