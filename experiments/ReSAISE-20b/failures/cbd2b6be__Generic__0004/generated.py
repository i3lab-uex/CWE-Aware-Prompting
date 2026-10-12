import urllib.parse

# Example list of allowed domains; replace or extend as needed.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # add other trusted domains here
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, token_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g. "https://app.example.com").
    redirect_path : str
        The path for the OAuth callback endpoint (e.g. "/oauth/callback").
    token_state : str
        A unique state value used to validate the OAuth flow.

    Returns
    -------
    str
        The fully qualified callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure redirect_path starts with a slash
    if not redirect_path.startswith("/"):
        redirect_path = "/" + redirect_path

    # Combine the base URL with the redirect path
    base_parsed = urllib.parse.urlparse(main_url)
    callback_url = urllib.parse.urljoin(base_parsed.geturl(), redirect_path)

    # Parse the combined URL to manipulate query parameters
    parsed = urllib.parse.urlparse(callback_url)
    # Preserve existing query params and add 'state'
    query_params = urllib.parse.parse_qs(parsed.query)
    # ``parse_qs`` returns lists; use simple dict for new param
    query_params["state"] = [token_state]
    # Encode back to a query string
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Rebuild the full URL with updated query
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

    # Validate domain against allowed list
    hostname = urllib.parse.urlparse(final_url).hostname or ""
    if hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Domain '{hostname}' is not allowed for OAuth callbacks."
        )

    return final_url