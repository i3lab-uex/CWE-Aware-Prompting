import urllib.parse

# Whitelist of domains that are allowed to receive the SSO redirect.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "myapp.local",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base URL of the SSO endpoint (may already contain query parameters).
    uid : str
        Unique user identifier.
    redirect_url : str
        Destination URL to which the identity provider should redirect after
        authentication.

    Returns
    -------
    str
        A fully‑formed URL that the client can use to initiate SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Extract the hostname for validation.  ``netloc`` may contain port numbers.
    host = parsed_redirect.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"redirect_url domain '{host}' is not allowed")

    # Parse the base SSO endpoint.
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Prepare query parameters.  Existing ones are preserved.
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # ``parse_qs`` returns lists; we want single values for new params.
    existing_params["uid"] = [uid]
    existing_params["redirect_url"] = [redirect_url]

    # Rebuild the query string.
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # Construct the final URL.
    sso_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return sso_url