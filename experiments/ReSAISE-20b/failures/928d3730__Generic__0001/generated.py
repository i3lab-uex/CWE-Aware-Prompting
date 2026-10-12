import urllib.parse

# Example set of allowed callback domains; adjust as needed for your application.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    host_url : str
        Base URL of the application (e.g., "https://myapp.com").
    path_callback : str
        Path to the OAuth callback handler (e.g., "/auth/callback").
    session_id : str
        Unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        Fully assembled OAuth callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS and
        does not match the host domain.
    """
    # Normalise the host URL to ensure it contains a scheme
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme:
        raise ValueError("host_url must include a scheme (e.g., 'https://')")
    host_netloc = parsed_host.netloc.lower()

    # Join the host URL with the callback path
    callback_url = urllib.parse.urljoin(host_url, path_callback)

    # Parse the resulting callback URL
    parsed_cb = urllib.parse.urlparse(callback_url)
    cb_netloc = parsed_cb.netloc.lower()

    # Validate domain: must be the same as host or in ALLOWED_CALLBACK_DOMAINS
    if cb_netloc != host_netloc and cb_netloc not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(
            f"Callback domain '{cb_netloc}' is not allowed. "
            "It must match the host or be in ALLOWED_CALLBACK_DOMAINS."
        )

    # Append the state parameter
    query_params = urllib.parse.parse_qs(parsed_cb.query, keep_blank_values=True)
    # Ensure we overwrite any existing state param for safety
    query_params["state"] = [session_id]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_cb.scheme,
            parsed_cb.netloc,
            parsed_cb.path,
            parsed_cb.params,
            new_query,
            parsed_cb.fragment,
        )
    )

    return final_url