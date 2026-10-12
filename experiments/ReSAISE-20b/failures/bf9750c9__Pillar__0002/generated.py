import urllib.parse

# Whitelist of domains that are allowed as return URLs after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted.partner.net",
}


def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct a full SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        The base URI of the SSO endpoint.
    user_identifier : str
        Unique identifier for the user (will be passed as a query parameter).
    redirect_link : str
        URL to which the user should be redirected after successful SSO.

    Returns
    -------
    str
        A fully constructed URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If the domain of ``redirect_link`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL's domain.
    parsed_redirect = urllib.parse.urlparse(redirect_link)
    # Extract the hostname (netloc may include port; we only care about host).
    domain = parsed_redirect.hostname
    if not domain or domain.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Return URL domain '{domain}' is not allowed.")

    # Encode the return link to safely include it as a query parameter.
    encoded_return = urllib.parse.quote(redirect_link, safe="")

    # Parse the SSO endpoint to manipulate its query string safely.
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Build new query parameters, preserving any existing ones.
    original_params = urllib.parse.parse_qs(parsed_sso.query)
    # Flatten parse_qs values (list) to single string.
    original_params = {k: v[0] for k, v in original_params.items()}

    # Add or override user identifier and return URL parameters.
    original_params.update(
        {
            "user": user_identifier,
            "return_url": encoded_return,
        }
    )

    # Reconstruct the full SSO URL with updated query string.
    new_query = urllib.parse.urlencode(original_params, doseq=False)
    new_sso_parts = parsed_sso._replace(query=new_query)

    return urllib.parse.urlunparse(new_sso_parts)