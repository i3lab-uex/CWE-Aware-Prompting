import urllib.parse

# Example whitelist – in real code this should be defined elsewhere and imported.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted.partner.net"
}

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        Base URL of the SSO provider.
    uid : str
        Unique user identifier to send to the SSO provider.
    redirect_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully‑qualified SSO URL containing the UID and encoded redirect target.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # ---- Validate the return URL domain ------------------------------------
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    # ``hostname`` returns the domain without port; ``netloc`` may contain port.
    redirect_domain = parsed_redirect.hostname
    if not redirect_domain or redirect_domain.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Return URL domain '{redirect_domain}' is not allowed")

    # ---- Build the SSO query parameters ------------------------------------
    parsed_auth = urllib.parse.urlparse(auth_endpoint)

    # Existing query parameters are preserved
    existing_params = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)

    # Add/overwrite the SSO specific parameters
    existing_params["uid"] = [uid]
    existing_params["redirect"] = [redirect_url]

    # urlencode will encode the values appropriately
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # ---- Reconstruct the full SSO URL --------------------------------------
    sso_url = urllib.parse.urlunparse((
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path,
        parsed_auth.params,
        new_query,
        parsed_auth.fragment
    ))

    return sso_url