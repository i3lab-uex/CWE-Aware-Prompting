import urllib.parse

# A set of domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The relative or absolute endpoint for the OAuth callback handler.
        If relative, it will be joined to ``main_url``. If absolute,
        its domain must still satisfy the allowed‑domain check.
    session_state : str
        A unique state token to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with the ``state`` query
        parameter appended.

    Raises
    ------
    ValueError
        If the final callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``
        or does not match the domain of ``main_url``.
    """
    # Parse the main application URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Resolve the redirect endpoint relative to the main URL
    resolved = urllib.parse.urljoin(main_url, redirect_endpoint)
    parsed_resolved = urllib.parse.urlparse(resolved)

    # Ensure the resolved URL has a valid scheme and netloc
    if not parsed_resolved.scheme or not parsed_resolved.netloc:
        raise ValueError(f"Invalid redirect_endpoint resulting in {resolved!r}")

    # Domain validation: must be the same as main_url or in the allowed list
    callback_domain = parsed_resolved.hostname.lower()
    main_domain = parsed_main.hostname.lower()

    if callback_domain != main_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {callback_domain!r} is not allowed "
            f"(must match main_url or be in ALLOWED_CALLBACK_DOMAINS)."
        )

    # Build query string with state parameter
    query = urllib.parse.urlencode({"state": session_state})

    # Reconstruct the final URL
    final_parts = list(parsed_resolved)
    final_parts[4] = query  # replace the existing query
    return urllib.parse.urlunparse(final_parts)