import urllib.parse

# Domains that are permitted for the return URL.  Add or remove as needed.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.example.org",
    "trusted.partner.net",
}


def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str,
) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    user_identifier : str
        Unique identifier for the user that will be passed to the SSO service.
    redirect_back_url : str
        URL to which the user should be redirected after authentication.

    Returns
    -------
    str
        A fully‑formed SSO redirect URL that includes the user identifier and
        a return URL as query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that the redirect_back_url domain is allowed.
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    return_domain = parsed_return.hostname
    if not return_domain:
        raise ValueError("Redirect back URL must contain a valid hostname.")

    # Check against allowed domains (case‑insensitive).
    if not any(return_domain.lower() == d.lower() or return_domain.lower().endswith("." + d.lower())
               for d in ALLOWED_RETURN_DOMAINS):
        raise ValueError(
            f"Return URL domain '{return_domain}' is not in the list of allowed domains."
        )

    # Build query parameters.
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url,
    }
    query_string = urllib.parse.urlencode(params, safe=":/?&")

    # Ensure the base SSO URL ends with a slash or query marker.
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("SSO service URL must be a valid absolute URL.")

    # Construct the final redirect link.
    base = urllib.parse.urlunparse(parsed_sso._replace(query=""))
    final_url = f"{base}?{query_string}"

    return final_url