import urllib.parse

# Domains that are allowed for the return URL. Adjust as needed.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.com",
    "myapp.org"
}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service.
    uid : str
        Unique identifier for the user. It will be passed as a query parameter.
    redirect_url : str
        URL to which the user should be sent after SSO. Must belong to an allowed domain.

    Returns
    -------
    str
        The fully‑qualified SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain
    parsed_return = urllib.parse.urlparse(redirect_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Extract the hostname (strip port if present)
    host = parsed_return.hostname
    if host is None:
        raise ValueError("redirect_url must contain a hostname")

    # Ensure the domain (or subdomain) is allowed
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not allowed")

    # Parse the SSO service base URL
    parsed_sso = urllib.parse.urlparse(sso_url)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("sso_url must be a valid absolute URL")

    # Prepare query parameters
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url  # the full URL is encoded
    }
    query_string = urllib.parse.urlencode(query_params, doseq=True)

    # Construct the final URL
    new_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path or "",
        parsed_sso.params,
        query_string,
        ""  # fragment
    ))
    return new_url

# Example usage:
if __name__ == "__main__":
    sso_base = "https://sso.example.com/login"
    user_id = "user-12345"
    return_to = "https://example.com/dashboard?view=home"

    try:
        url = create_sso_redirect_url(sso_base, user_id, return_to)
        print("SSO redirect URL:", url)
    except ValueError as e:
        print("Error:", e)