import urllib.parse

# Domains that are allowed to receive the SSO redirect.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    uid : str
        Unique identifier of the user.
    redirect_url : str
        URL to return to after successful SSO.

    Returns
    -------
    str
        The full redirect URL that should be sent to the user.

    Raises
    ------
    ValueError
        If ``redirect_url`` points to a domain not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that the return URL's domain is allowed.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect URL format.")

    # Extract the hostname (exclude port if present)
    host = parsed_redirect.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Construct query parameters
    params = {
        "uid": uid,
        "redirect_uri": redirect_url,  # the original URL will be re‑encoded
    }

    # Build the final SSO URL: keep existing query in sso_url, if any
    parsed_sso = urllib.parse.urlparse(sso_url)
    existing_query = dict(urllib.parse.parse_qsl(parsed_sso.query))
    # Merge: new params override existing ones
    merged_query = {**existing_query, **params}
    encoded_query = urllib.parse.urlencode(merged_query)

    # Reconstruct the SSO URL with the new query string
    final_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            encoded_query,
            parsed_sso.fragment,
        )
    )

    return final_url