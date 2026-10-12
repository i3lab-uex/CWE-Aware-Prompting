import urllib.parse

# Example allowed domains – in real usage this would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def assemble_oauth_callback(application_url: str, callback_route: str, token_state: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The relative or absolute path that handles the OAuth callback
        (e.g. "/oauth/callback" or "https://app.example.com/oauth/callback").
    token_state : str
        A unique string that will be added as the `state` query parameter.

    Returns
    -------
    str
        The fully assembled OAuth callback URL including the `state` parameter.

    Raises
    ------
    ValueError
        If the callback URL domain is not in ``ALLOWED_CALLBACK_DOMAINS`` or if it
        does not match the domain of ``application_url``.
    """
    # Ensure application_url is a full URL
    parsed_app = urllib.parse.urlparse(application_url)
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError(f"Invalid application_url: {application_url!r}")

    # Resolve the callback route against the application URL
    joined = urllib.parse.urljoin(application_url, callback_route)
    parsed_cb = urllib.parse.urlparse(joined)

    # Validate that the callback URL has a scheme and netloc
    if not parsed_cb.scheme or not parsed_cb.netloc:
        raise ValueError(f"Invalid callback URL after resolution: {joined!r}")

    # Domain checks
    app_domain = parsed_app.netloc.lower()
    cb_domain = parsed_cb.netloc.lower()

    # 1. Must be the same domain as the application
    if cb_domain != app_domain:
        raise ValueError(
            f"Callback domain {cb_domain!r} does not match application domain {app_domain!r}"
        )

    # 2. Must be in the allowed callback domains list
    if app_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Application domain {app_domain!r} is not in the allowed callback domains"
        )

    # Construct query string with state
    query = urllib.parse.urlencode({"state": token_state})
    # Preserve existing query parameters if any
    if parsed_cb.query:
        new_query = f"{parsed_cb.query}&{query}"
    else:
        new_query = query

    # Rebuild the final URL
    assembled = urllib.parse.urlunparse(
        (
            parsed_cb.scheme,
            parsed_cb.netloc,
            parsed_cb.path,
            parsed_cb.params,
            new_query,
            parsed_cb.fragment,
        )
    )

    return assembled