import urllib.parse

# Example whitelist of domains allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.org",
    "app.example.net"
}


def _extract_domain(url: str) -> str:
    """
    Return the network location (netloc) part of a URL, lower‑cased and stripped
    of any leading 'www.' prefix for comparison purposes.
    """
    parsed = urllib.parse.urlparse(url)
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


def construct_sso_redirect(sso_uri: str, user_identifier: str, redirect_link: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint URL.
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_link : str
        URL to return to after successful SSO.

    Returns
    -------
    str
        Fully‑qualified redirect URL with query parameters safely encoded.

    Raises
    ------
    ValueError
        If the redirect_link domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate that the redirect link domain is allowed
    redirect_domain = _extract_domain(redirect_link)
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{redirect_domain}' is not permitted for SSO return URLs."
        )

    # Parse the base SSO URI so we can safely append query parameters
    parsed_sso = urllib.parse.urlparse(sso_uri)

    # Prepare the new query parameters
    query_params = {
        "user": user_identifier,
        "return_url": redirect_link,
    }

    # Merge with any existing query parameters on the SSO endpoint
    existing_params = urllib.parse.parse_qs(parsed_sso.query)
    # Flatten parse_qs result (values are lists) into a simple dict
    existing_params = {k: v[0] for k, v in existing_params.items()}
    merged_params = {**existing_params, **query_params}

    # Build the new query string
    encoded_query = urllib.parse.urlencode(merged_params, doseq=True)

    # Reconstruct the full URL
    new_url = urllib.parse.urlunparse(
        parsed_sso._replace(query=encoded_query)
    )

    return new_url