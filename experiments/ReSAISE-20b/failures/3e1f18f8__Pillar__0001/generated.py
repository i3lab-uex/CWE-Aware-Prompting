import urllib.parse

# Example set of allowed domains; replace with your actual list.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

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
        The base URL of the SSO provider.
    user_identifier : str
        Unique identifier for the user (e.g., username or UUID).
    redirect_uri : str
        Absolute URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The full redirect URL ready to be used in an HTTP redirect.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URI to validate its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_uri must be a fully-qualified URL")

    domain = parsed_redirect.netloc.split(":")[0].lower()
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for redirect_uri")

    # Build the query parameters.
    params = {
        "user": user_identifier,
        "redirect_uri": redirect_uri
    }
    encoded_params = urllib.parse.urlencode(params, safe=":/?=&")

    # Parse the SSO endpoint to correctly append parameters.
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)
    if parsed_endpoint.scheme not in {"http", "https"}:
        raise ValueError("auth_service_endpoint must use http or https scheme")

    # Merge existing query parameters with the new ones.
    existing_query = urllib.parse.parse_qs(parsed_endpoint.query, keep_blank_values=True)
    # Convert list values to single strings for simplicity.
    existing_query = {k: v[0] if isinstance(v, list) else v for k, v in existing_query.items()}
    merged_query = urllib.parse.urlencode(existing_query) + ("&" if existing_query else "") + encoded_params

    # Reconstruct the full URL.
    final_url = urllib.parse.urlunparse(
        parsed_endpoint._replace(query=merged_query)
    )
    return final_url