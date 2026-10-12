import urllib.parse

# Example allowed domains; replace or import from your configuration.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user (e.g., a UUID).
    back_url : str
        URL to redirect to after the SSO process completes.

    Returns
    -------
    str
        A fully-formed URL that points to the SSO service and includes the
        `user_ref` and a safe, encoded return URL.

    Raises
    ------
    ValueError
        If the `back_url` does not have an allowed domain or is malformed.
    """
    # Validate that back_url is absolute and has a scheme
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError(f"Invalid back_url: {back_url!r}")

    # Extract the hostname (domain) and compare against allowed domains
    domain = parsed_back.hostname.lower() if parsed_back.hostname else ""
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters, ensuring proper percent‑encoding
    query_params = {
        "user_ref": user_ref,
        "return_url": back_url,   # will be percent‑encoded by urlencode
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Construct the final URL
    parsed_sso = urllib.parse.urlparse(sso_service)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError(f"Invalid sso_service URL: {sso_service!r}")

    # Preserve any existing path/query/hash in the sso_service
    final_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path or "",
        "",  # params
        encoded_query,
        ""   # fragment
    ))
    return final_url