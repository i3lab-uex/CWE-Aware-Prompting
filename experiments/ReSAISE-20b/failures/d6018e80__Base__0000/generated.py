import urllib.parse

# Set of domains that are allowed for the return URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL that safely includes the user ID
    and a return URL. The function validates that the return URL's domain is in
    `ALLOWED_RETURN_DOMAINS` to mitigate open‑redirect vulnerabilities (CWE‑601).

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (may already contain query parameters).
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication. Must be a fully qualified URL.

    Returns
    -------
    str
        A complete SSO redirect URL containing the user ID and return URL as query parameters.

    Raises
    ------
    ValueError
        If `redirect_url` is not a valid absolute URL or its domain is not in
        `ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL and ensure it is absolute.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not (parsed_redirect.scheme and parsed_redirect.netloc):
        raise ValueError("redirect_url must be an absolute URL with scheme and host")

    # Verify the domain is allowed.
    redirect_domain = parsed_redirect.netloc.lower()
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{redirect_domain}' is not allowed")

    # Build the query parameters.
    params = {
        "uid": uid,
        "redirect": redirect_url
    }
    query_string = urllib.parse.urlencode(params)

    # Parse the base SSO URL to preserve existing query parameters.
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Merge existing query with new parameters.
    if parsed_sso.query:
        combined_query = f"{parsed_sso.query}&{query_string}"
    else:
        combined_query = query_string

    # Reconstruct the full SSO URL.
    new_sso_parts = parsed_sso._replace(query=combined_query)
    final_url = urllib.parse.urlunparse(new_sso_parts)

    return final_url