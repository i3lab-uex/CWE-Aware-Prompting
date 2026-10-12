import urllib.parse

# Example whitelist – replace with your actual domains.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL (e.g., "https://auth.example.com/sso").
    uid : str
        The unique identifier for the user.
    redirect_url : str
        The URL to return to after authentication.

    Returns
    -------
    str
        A fully-formed SSO redirect URL containing the uid and a
        percent‑encoded return URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    redirect_domain = parsed_redirect.netloc.split(':')[0].lower()

    # Verify the domain is in the whitelist.
    if redirect_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{redirect_domain}' is not allowed."
        )

    # Build query parameters safely.
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }
    encoded_params = urllib.parse.urlencode(query_params, safe=':/?&=#')

    # Ensure the SSO path does not already contain a query string.
    base_url, _, existing_query = sso_path.partition('?')
    if existing_query:
        # Append to the existing query string.
        final_url = f"{base_url}?{existing_query}&{encoded_params}"
    else:
        final_url = f"{sso_path}?{encoded_params}"

    return final_url