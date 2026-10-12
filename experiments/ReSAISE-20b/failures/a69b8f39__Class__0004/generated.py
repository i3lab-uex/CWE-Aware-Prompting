import urllib.parse

# Domains that are allowed to be used as a return URL after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build an SSO redirect URL that includes the user reference and a safe return URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to redirect to after SSO. Must belong to an allowed domain.

    Returns
    -------
    str
        Full URL that can be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If ``back_url`` points to a domain that is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the return URL to inspect its domain.
    parsed_back = urllib.parse.urlparse(back_url)

    # If the back URL is relative (no netloc), treat it as safe.
    if parsed_back.netloc:
        # Extract the hostname, ignoring any port number.
        host = parsed_back.hostname or ""
        if host.lower() not in ALLOWED_RETURN_DOMAINS:
            raise ValueError(
                f"Return URL domain '{host}' is not allowed. "
                f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
            )

    # Prepare query parameters. Use quote_plus for back_url to handle special chars.
    params = {
        "user_ref": user_ref,
        "back_url": back_url,
    }
    query_string = urllib.parse.urlencode(params, doseq=True)

    # Construct the final redirect URL.
    base = sso_service.rstrip("?")  # avoid duplicate question marks
    return f"{base}?{query_string}"