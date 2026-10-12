import urllib.parse

# Domains that are allowed to be used as the return URL after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trustedpartner.net",
}


def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (must be an absolute URL).
    user_identifier : str
        Unique identifier for the user.
    redirect_back_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to initiate the SSO flow.

    Raises
    ------
    ValueError
        If `redirect_back_url` does not belong to an allowed domain.
    """

    # Validate that the SSO service URL is absolute
    sso_parsed = urllib.parse.urlparse(sso_service_url)
    if not sso_parsed.scheme or not sso_parsed.netloc:
        raise ValueError("sso_service_url must be an absolute URL")

    # Parse the return URL and validate its domain
    redirect_parsed = urllib.parse.urlparse(redirect_back_url)
    if not redirect_parsed.scheme or not redirect_parsed.netloc:
        raise ValueError("redirect_back_url must be an absolute URL")

    # Extract the hostname (e.g., 'sub.example.com') and compare with allowed domains
    hostname = redirect_parsed.hostname or ""
    # Allow subdomains of the permitted domains
    if not any(hostname == domain or hostname.endswith("." + domain)
               for domain in ALLOWED_RETURN_DOMAINS):
        raise ValueError(
            f"Return URL domain '{hostname}' is not in the list of allowed domains"
        )

    # Build query parameters
    params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_back_url
    }
    query_string = urllib.parse.urlencode(params)

    # Construct the final redirect URL
    if sso_parsed.query:
        # Preserve existing query parameters on the SSO service URL
        base = sso_service_url.split("?", 1)[0]
    else:
        base = sso_service_url

    final_url = f"{base}?{query_string}"
    return final_url