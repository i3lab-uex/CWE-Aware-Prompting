import urllib.parse

# Set of domains that are allowed to be used as the redirect target.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def _extract_domain(url: str) -> str:
    """
    Extract the hostname (domain) from a URL.
    """
    parsed = urllib.parse.urlparse(url)
    # hostname is already lower‑cased by urlparse
    return parsed.hostname or ""

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

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
        A fully formed URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the return URL domain
    target_domain = _extract_domain(redirect_url)
    if target_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{target_domain}' is not allowed."
        )

    # Parse the auth endpoint to preserve existing query parameters
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    # Existing query params as a dict
    existing_params = dict(urllib.parse.parse_qsl(parsed_auth.query, keep_blank_values=True))

    # Add/overwrite the required parameters
    existing_params["uid"] = uid
    existing_params["redirect"] = redirect_url

    # Build the new query string
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # Reconstruct the full URL
    new_auth = parsed_auth._replace(query=new_query)
    return urllib.parse.urlunparse(new_auth)

# Example usage:
if __name__ == "__main__":
    endpoint = "https://sso.example.com/auth"
    user_id = "user12345"
    return_url = "https://app.example.com/home"

    redirect_link = build_sso_redirect(endpoint, user_id, return_url)
    print(redirect_link)