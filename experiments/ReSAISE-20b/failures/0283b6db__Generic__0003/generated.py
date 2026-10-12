import urllib.parse

# Set of domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "app.example.org"}


def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service endpoint.
    user_id : str
        The unique identifier for the user.
    return_url : str
        The URL to redirect back to after successful SSO.

    Returns
    -------
    str
        A fully‑qualified URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If ``return_url`` does not belong to an allowed domain.
    """
    # Parse the return URL and validate its domain
    parsed_return = urllib.parse.urlparse(return_url)
    hostname = parsed_return.hostname

    if not hostname or hostname.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Encode the return URL so it can safely be passed as a query parameter
    encoded_return = urllib.parse.quote_plus(return_url)

    # Encode the user_id in case it contains special characters
    encoded_user = urllib.parse.quote_plus(user_id)

    # Build the final SSO redirect URL
    # Preserve any existing query parameters on the endpoint
    parsed_endpoint = urllib.parse.urlparse(sso_endpoint)
    base_query = dict(urllib.parse.parse_qsl(parsed_endpoint.query))
    # Add our parameters
    base_query.update(
        {
            "user_id": encoded_user,
            "return_url": encoded_return,
        }
    )
    # Reconstruct the full URL
    new_query = urllib.parse.urlencode(base_query)
    final_url = urllib.parse.urlunparse(
        (
            parsed_endpoint.scheme,
            parsed_endpoint.netloc,
            parsed_endpoint.path,
            parsed_endpoint.params,
            new_query,
            parsed_endpoint.fragment,
        )
    )

    return final_url