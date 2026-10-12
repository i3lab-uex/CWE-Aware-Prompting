import urllib.parse

# Whitelisted domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {"example.com", "app.example.org"}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint (e.g., "https://sso.example.com/auth").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the user should be sent after authentication.

    Returns
    -------
    str
        Fully constructed SSO URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to validate its domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Extract the hostname (strip port if present)
    host = parsed_redirect.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{host}' is not allowed")

    # Build the query parameters for the SSO endpoint
    sso_params = {
        "uid": uid,
        # The return URL must be percent‑encoded to preserve its structure
        "return": redirect_url,
    }

    # Merge existing query parameters from sso_path (if any)
    parsed_sso = urllib.parse.urlparse(sso_path)
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))
    merged_params = {**existing_params, **sso_params}

    # Reconstruct the full SSO URL
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    full_sso_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return full_sso_url