import urllib.parse

# Example allowed domains; in a real application this would be configured elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "sub.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. https://app.example.com).
    redirect_endpoint : str
        The relative or absolute path to the OAuth callback handler.
    session_state : str
        A unique state string used to protect against CSRF.

    Returns
    -------
    str
        The fully assembled, validated OAuth callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not allowed or does not match the
        application's domain.
    """
    # Parse the base URL and ensure it is absolute.
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("main_url must be a fully-qualified absolute URL")

    # Resolve the redirect endpoint against the base URL.
    joined_url = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Append the state parameter in a safe manner.
    parsed_joined = urllib.parse.urlparse(joined_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_joined.query, keep_blank_values=True))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    final_url = parsed_joined._replace(query=new_query).geturl()

    # Validate the domain of the final URL.
    parsed_final = urllib.parse.urlparse(final_url)
    callback_domain = parsed_final.hostname

    if not callback_domain:
        raise ValueError("Callback URL does not contain a valid hostname")

    # Allow the callback only if it is on the same domain as the main URL
    # or on one of the explicitly allowed domains.
    if callback_domain != parsed_main.hostname and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed for redirects"
        )

    return final_url