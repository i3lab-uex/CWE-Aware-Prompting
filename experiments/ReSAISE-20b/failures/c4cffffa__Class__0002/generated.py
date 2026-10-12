import urllib.parse

# Domains that are permitted to be used as the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    # Add more domains as needed
}


def _is_allowed_domain(url: str) -> bool:
    """
    Verify that the given URL belongs to one of the allowed return domains.
    """
    parsed = urllib.parse.urlparse(url)
    # Extract hostname (netloc may include port).
    hostname = parsed.hostname
    if not hostname:
        return False
    # Compare the hostname against the allowed set.
    return hostname.lower() in ALLOWED_RETURN_DOMAINS


def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str,
) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (must include scheme and host).
    user_identifier : str
        Unique identifier for the user.
    redirect_back_url : str
        URL to return to after SSO authentication.

    Returns
    -------
    str
        Fully formed redirect URL.

    Raises
    ------
    ValueError
        If the return URL's domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Ensure that the SSO service URL is well‑formed.
    sso_parsed = urllib.parse.urlparse(sso_service_url)
    if not (sso_parsed.scheme and sso_parsed.netloc):
        raise ValueError("Invalid SSO service URL")

    # Validate the redirect_back_url domain.
    if not _is_allowed_domain(redirect_back_url):
        raise ValueError(
            f"Return URL domain '{urllib.parse.urlparse(redirect_back_url).hostname}' "
            "is not allowed."
        )

    # Build query parameters.
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url,
    }
    query = urllib.parse.urlencode(params, safe="/:")

    # Construct the final URL.
    redirect_url = urllib.parse.urlunparse(
        (
            sso_parsed.scheme,
            sso_parsed.netloc,
            sso_parsed.path.rstrip("/") + "/auth",
            sso_parsed.params,
            query,
            sso_parsed.fragment,
        )
    )

    return redirect_url