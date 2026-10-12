import urllib.parse

# Whitelist of domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    # add more approved domains here
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct a full SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base URL (or path) of the SSO endpoint.
    uid : str
        Unique user identifier to be sent to the identity provider.
    redirect_url : str
        The URL that the user should be returned to after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Normalize domain for comparison (case‑insensitive)
    redirect_domain = parsed_redirect.netloc.lower()
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{redirect_domain}' is not allowed for redirect URLs")

    # Parse the SSO endpoint URL
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Merge existing query parameters with the new ones
    query_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # parse_qs returns lists for each key; we want single values
    flat_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

    # Add/overwrite uid and redirect parameters
    flat_params.update({
        "uid": uid,
        # Use full URL as a single string; urlencode will escape it
        "redirect": redirect_url,
    })

    # Build the new query string
    encoded_query = urllib.parse.urlencode(flat_params, doseq=True)

    # Reconstruct the full SSO URL
    new_sso = parsed_sso._replace(query=encoded_query)
    full_url = urllib.parse.urlunparse(new_sso)

    return full_url