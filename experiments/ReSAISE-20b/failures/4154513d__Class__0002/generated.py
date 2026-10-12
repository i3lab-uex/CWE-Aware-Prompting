import urllib.parse

# Allowed domains for the redirect URL (e.g., "example.com", "app.example.org")
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO service.
    uid : str
        The unique identifier for the user.
    redirect_url : str
        The URL to which users should be returned after authentication.

    Returns
    -------
    str
        A fully formed redirect URL containing the required query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain (hostname)
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    hostname = parsed_redirect.hostname

    if not hostname or hostname.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect URL domain '{hostname}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Prepare query parameters for the SSO endpoint
    params = {
        "uid": uid,
        # Ensure redirect URL is percent‑encoded
        "redirect_uri": redirect_url,
    }

    # Encode the parameters safely
    query_string = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=")

    # Combine the auth endpoint with the query string
    if urllib.parse.urlparse(auth_endpoint).scheme == "":
        raise ValueError("auth_endpoint must be a valid URL with scheme (http/https).")

    # Append the query string to the auth endpoint
    redirect_to = (
        f"{auth_endpoint.rstrip('?')}"
        f"?{query_string}" if not auth_endpoint.endswith("?") else f"{auth_endpoint}{query_string}"
    )

    return redirect_to