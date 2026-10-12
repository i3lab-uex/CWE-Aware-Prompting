import urllib.parse

# Set of domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the third‑party SSO service.
    user_ref : str
        Unique identifier for the user (e.g., a UUID or username).
    back_url : str
        URL to return to after the SSO process.

    Returns
    -------
    str
        The full URL that should be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If `back_url` does not belong to an allowed domain.
    """
    # Parse the return URL and validate its hostname
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("Invalid return URL format.")

    # Extract hostname (including subdomains)
    host = parsed_back.hostname.lower()
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed.")

    # Build query parameters, ensuring they are properly encoded
    params = {
        "user_ref": user_ref,
        # The back_url itself must be URL‑encoded so that it can safely
        # travel as a query value.
        "back_url": back_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?&=")

    # Construct the final redirect URL
    base = urllib.parse.urlparse(sso_service)
    # Preserve any existing query parameters on the SSO service URL
    new_query = urllib.parse.urlencode(
        dict(urllib.parse.parse_qsl(base.query)), doseq=True
    )
    if new_query:
        query_string = f"{new_query}&{query_string}"

    redirect_url = urllib.parse.urlunparse(
        (base.scheme, base.netloc, base.path, base.params, query_string, "")
    )
    return redirect_url