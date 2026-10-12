import urllib.parse

# Set of domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def assemble_oauth_callback_url(
    root_url: str,
    path_for_callback: str,
    session_token: str
) -> str:
    """
    Build a full OAuth callback URL.

    Parameters
    ----------
    root_url : str
        Base URL of the application, e.g. "https://myapp.com".
    path_for_callback : str
        Path that will handle the OAuth callback, e.g. "/auth/callback".
    session_token : str
        Token used as the `state` parameter to protect against CSRF.

    Returns
    -------
    str
        Fully qualified callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL does not belong to an allowed domain.
    """
    # Normalise the root URL (ensure it ends with a slash for urljoin)
    if not root_url.endswith("/"):
        root_url += "/"

    # Join the base URL with the callback path
    full_path = urllib.parse.urljoin(root_url, path_for_callback.lstrip("/"))

    # Append the state query parameter
    parsed = urllib.parse.urlparse(full_path)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = session_token
    new_query = urllib.parse.urlencode(query_params)

    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    # Validate the domain
    if parsed.netloc.split(":")[0] not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {parsed.netloc}")

    return final_url