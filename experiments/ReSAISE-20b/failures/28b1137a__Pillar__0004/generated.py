import urllib.parse

# Whitelist of domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL.
    uid : str
        Unique user identifier to be sent to the identity provider.
    redirect_url : str
        Destination URL where the user should be returned after authentication.

    Returns
    -------
    str
        The full SSO redirect URL including query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL's domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a fully qualified URL")

    # Extract domain (hostname) and compare against the whitelist.
    hostname = parsed_redirect.hostname
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{hostname}' is not allowed")

    # Build query parameters for the SSO request.
    params = {
        "uid": uid,
        # Encode the redirect URL to avoid issues with special characters.
        "redirect_url": urllib.parse.quote(redirect_url, safe=""),
    }

    # Parse the base SSO path to preserve any existing components.
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Merge existing query parameters if present.
    existing_qs = urllib.parse.parse_qs(parsed_sso.query)
    # Convert list values to single strings for simplicity.
    existing_qs = {k: v[0] for k, v in existing_qs.items()}
    merged_params = {**existing_qs, **params}

    # Construct the new query string.
    new_query = urllib.parse.urlencode(merged_params)

    # Rebuild the full URL with updated query.
    new_sso_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return new_sso_url