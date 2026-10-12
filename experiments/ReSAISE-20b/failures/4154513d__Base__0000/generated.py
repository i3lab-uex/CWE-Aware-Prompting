import urllib.parse

# Set of domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO service endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        The URL to which users should be returned after authentication.

    Returns
    -------
    str
        A fully-formed redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Parse the return URL to inspect its components
    parsed = urllib.parse.urlparse(redirect_url)

    # Reject URLs without a scheme (e.g., relative paths) or with an untrusted domain
    if not parsed.scheme:
        raise ValueError("Redirect URL must be absolute with a scheme (http/https).")

    # Only allow http or https schemes
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Redirect URL scheme must be http or https.")

    # Extract the hostname (netloc may include port)
    host = parsed.hostname
    if not host:
        raise ValueError("Redirect URL must contain a valid hostname.")

    # Normalize the host to lowercase for comparison
    host = host.lower()

    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect URL domain '{host}' is not allowed.")

    # Encode the return_url so it can safely be embedded as a query parameter
    encoded_return = urllib.parse.quote(redirect_url, safe="")

    # Construct the final redirect URL
    query = urllib.parse.urlencode({"uid": uid, "redirect": encoded_return})
    final_url = f"{auth_endpoint.rstrip('/')}/?{query}"

    return final_url