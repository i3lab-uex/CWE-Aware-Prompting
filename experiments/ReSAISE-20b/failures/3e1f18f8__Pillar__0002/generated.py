import urllib.parse

# Domains that are allowed to be used as the redirect target.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
}

def _extract_domain(url: str) -> str:
    """
    Return the hostname part of a URL. Raises ValueError if the URL is not
    absolute or does not contain a hostname.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Redirect URL must be absolute: {url!r}")
    return parsed.hostname or ""

def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base endpoint of the SSO service (must be an absolute URL).
    user_identifier : str
        Unique identifier for the user.
    redirect_uri : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully constructed redirect URL ready to be sent to the client.

    Raises
    ------
    ValueError
        If `redirect_uri` contains a domain that is not in
        :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the SSO endpoint is absolute
    sso_parsed = urllib.parse.urlparse(auth_service_endpoint)
    if not sso_parsed.scheme or not sso_parsed.netloc:
        raise ValueError(f"SSO endpoint must be absolute: {auth_service_endpoint!r}")

    # Validate the redirect_uri domain
    target_domain = _extract_domain(redirect_uri).lower()
    if target_domain not in {d.lower() for d in ALLOWED_RETURN_DOMAINS}:
        raise ValueError(
            f"Redirect domain '{target_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Build query parameters
    query = urllib.parse.urlencode(
        {
            "user_id": user_identifier,
            "redirect_uri": redirect_uri,  # urllib.parse.urlencode will quote it
        },
        doseq=False,
    )

    # Construct the final URL. Preserve any existing query/path fragments.
    base = urllib.parse.urlunparse(
        (
            sso_parsed.scheme,
            sso_parsed.netloc,
            sso_parsed.path.rstrip("/") + "/sso",  # typical endpoint path
            "",  # params
            query,
            "",  # fragment
        )
    )

    return base

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = construct_sso_redirect(
#         "https://sso.example.com",
#         "user123",
#         "https://app.example.org/dashboard"
#     )
#     print(url)