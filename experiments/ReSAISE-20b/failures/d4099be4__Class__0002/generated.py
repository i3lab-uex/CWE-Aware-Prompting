import urllib.parse

# Example allowed domains – in a real project these would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.myapp.org"}

def generate_oauth_callback_link(app_base_url: str,
                                 callback_endpoint: str,
                                 verification_state: str) -> str:
    """
    Construct a fully‑qualified OAuth callback URL and ensure its domain is trusted.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    callback_endpoint : str
        The relative path for the OAuth callback (e.g., "/oauth/callback").
    verification_state : str
        A unique opaque value used to prevent CSRF.

    Returns
    -------
    str
        The fully‑qualified callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the base URL (ensure it has a scheme and no trailing slash)
    parsed_base = urllib.parse.urlparse(app_base_url.rstrip("/"))
    if not parsed_base.scheme:
        raise ValueError("app_base_url must include a scheme (http:// or https://)")

    # Build the absolute callback URL using urljoin
    absolute_url = urllib.parse.urljoin(parsed_base.geturl(), callback_endpoint.lstrip("/"))

    # Append the state query parameter
    parsed_url = urllib.parse.urlparse(absolute_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_url.query))
    query_params["state"] = verification_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the full URL with the updated query string
    final_url = urllib.parse.urlunparse(
        parsed_url._replace(query=new_query)
    )

    # Verify the domain is allowed
    if parsed_base.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {parsed_base.netloc}. "
            f"Allowed domains are: {', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return final_url