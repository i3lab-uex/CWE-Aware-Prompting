import urllib.parse

# Domains that are allowed to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
    # add more trusted domains here
}


def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (may already contain query parameters).
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully-formed SSO redirect URL with the user ID and return URL as query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # 1. Validate the return URL domain
    parsed_return = urllib.parse.urlparse(redirect_url)
    # Extract just the hostname (without port)
    domain = parsed_return.hostname
    if not domain or domain.lower() not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # 2. Parse the base SSO URL
    parsed_sso = urllib.parse.urlparse(sso_url)

    # 3. Merge existing query parameters with the new ones
    existing_qs = urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True)
    # Append the required parameters
    new_qs = existing_qs + [
        ("uid", uid),
        ("return_url", redirect_url),  # this will be URL‑encoded by urlencode
    ]

    # 4. Reconstruct the full SSO redirect URL
    encoded_qs = urllib.parse.urlencode(new_qs, doseq=True)
    new_url_parts = (
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        encoded_qs,
        parsed_sso.fragment,
    )
    return urllib.parse.urlunparse(new_url_parts)