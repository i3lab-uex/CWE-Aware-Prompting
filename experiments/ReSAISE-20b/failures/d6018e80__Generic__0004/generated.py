import urllib.parse

# Domains that are allowed to be used as a return URL after SSO authentication
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted-domain.net",
}

def _extract_domain(url: str) -> str:
    """
    Extract the domain part (netloc without port) from a URL.
    Raises ValueError if the URL is malformed or does not contain a host.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url!r}")

    # netloc may contain port; strip it
    host = parsed.hostname
    if not host:
        raise ValueError(f"Could not determine hostname in URL: {url!r}")
    return host.lower()


def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        The base URL of the SSO service (e.g. "https://sso.example.com/login").
    uid : str
        The unique identifier for the user.
    redirect_url : str
        The URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        A fully‑formed URL that can be sent to the client for redirection.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL's domain
    domain = _extract_domain(redirect_url)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain {domain!r} is not allowed")

    # Parse the SSO base URL
    parsed_sso = urllib.parse.urlparse(sso_url)

    # Build query parameters.  We use quote_plus to safely encode values.
    params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }
    query_string = urllib.parse.urlencode(params, doseq=True)

    # Assemble the final URL
    new_parts = parsed_sso._replace(query=query_string)
    return urllib.parse.urlunparse(new_parts)


# Example usage (commented out; remove comments to test)
# if __name__ == "__main__":
#     url = create_sso_redirect_url(
#         sso_url="https://sso.example.com/login",
#         uid="user-1234",
#         redirect_url="https://myapp.org/dashboard"
#     )
#     print(url)