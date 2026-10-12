import urllib.parse

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    "localhost",  # useful for local development
}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str,
                             session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The path or full URL for the OAuth callback handler (e.g. "/auth/callback").
    session_state : str
        A unique token used to validate the OAuth exchange.

    Returns
    -------
    str
        The fully formed callback URL, including a ``state`` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``
        and does not match the domain of ``main_url``.
    """
    # Resolve the callback URL relative to the main application root
    full_callback = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_endpoint.lstrip('/'))

    # Parse the URL components
    parsed = urllib.parse.urlparse(full_callback)

    # Validate domain: must be in allowed list or match the main URL's domain
    callback_domain = parsed.hostname.lower() if parsed.hostname else ''
    main_parsed = urllib.parse.urlparse(main_url)
    main_domain = main_parsed.hostname.lower() if main_parsed.hostname else ''

    allowed = (
        callback_domain in ALLOWED_CALLBACK_DOMAINS
        or callback_domain == main_domain
    )
    if not allowed:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not permitted for OAuth redirects."
        )

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # Ensure existing state values are overridden
    query_params['state'] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        )
    )

    return final_url

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = build_oauth_redirect_url(
#         main_url="https://app.example.com",
#         redirect_endpoint="/oauth/callback",
#         session_state="abc123"
#     )
#     print(url)