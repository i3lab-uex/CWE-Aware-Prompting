import urllib.parse

# Example set of allowed callback domains. In real use, populate with your own domain names.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a fully qualified OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_path : str
        The path to handle OAuth callbacks (e.g., "/auth/callback").
    nonce : str
        A state token used to prevent CSRF attacks.

    Returns
    -------
    str
        The complete callback URL including scheme, host, path and query parameters.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Construct the base URL (scheme + netloc)
    parsed_main = urllib.parse.urlparse(main_url.rstrip("/"))
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("main_url must contain a scheme and host")

    # Resolve the redirect path against the main URL
    callback_url = urllib.parse.urljoin(parsed_main.geturl(), redirect_path.lstrip("/"))

    # Append the nonce as a query parameter named 'state'
    parsed_callback = urllib.parse.urlparse(callback_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_callback.query))
    query_params["state"] = nonce
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the final URL with updated query
    final_url = urllib.parse.urlunparse((
        parsed_callback.scheme,
        parsed_callback.netloc,
        parsed_callback.path,
        parsed_callback.params,
        new_query,
        parsed_callback.fragment
    ))

    # Validate the domain against allowed domains (CWE-610 mitigation)
    domain = parsed_callback.netloc.split(":")[0]  # strip port if present
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{domain}' is not authorized")

    return final_url