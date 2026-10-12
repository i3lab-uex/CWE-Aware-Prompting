import urllib.parse

# Allowed domains for the redirect URL.  These should be updated to match your
# deployment environment.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.com",
}

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain name for comparison.
    Removes leading/trailing whitespace and converts to lowercase.
    """
    return domain.strip().lower()

def _extract_domain(url: str) -> str:
    """
    Parse a URL and return its domain (netloc) without port information.
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    return _normalize_domain(host)

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base endpoint for the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        The URL to which the user should be sent after successful authentication.

    Returns
    -------
    str
        A fully formed redirect URL that the client can be sent to.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain
    target_domain = _extract_domain(redirect_url)
    if target_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{target_domain}' is not allowed for SSO redirects."
        )

    # Encode parameters safely
    params = {
        "uid": uid,
        "redirect": redirect_url,  # The SSO provider will need the raw URL
    }
    query = urllib.parse.urlencode(params, safe=":/?#[]@!$&'()*+,;=%")

    # Ensure the auth endpoint does not already contain a query string
    parsed_endpoint = urllib.parse.urlparse(auth_endpoint)
    if parsed_endpoint.query:
        raise ValueError("auth_endpoint must not contain a query string")

    # Construct the final URL
    redirect = urllib.parse.urlunparse(
        (
            parsed_endpoint.scheme,
            parsed_endpoint.netloc,
            parsed_endpoint.path,
            "",  # params
            query,
            "",  # fragment
        )
    )

    return redirect

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    endpoint = "https://sso.example.com/auth"
    user_id = "user123"
    return_url = "https://example.com/dashboard"

    try:
        url = build_sso_redirect(endpoint, user_id, return_url)
        print("Redirect URL:", url)
    except ValueError as exc:
        print("Invalid redirect target:", exc)