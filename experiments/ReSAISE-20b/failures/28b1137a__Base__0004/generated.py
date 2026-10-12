import urllib.parse

# Whitelist of domains allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add more domains as needed
}


def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL that includes the user ID and a return URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL (may contain existing query parameters).
    uid : str
        Unique user identifier to be sent to the SSO provider.
    redirect_url : str
        The URL where the user should be returned after successful SSO.

    Returns
    -------
    str
        The fully assembled SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    domain = parsed_redirect.netloc.split(":")[0].lower()  # strip port if present
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect URL domain '{domain}' is not allowed.")

    # Parse the SSO path to manipulate query parameters
    parsed_sso = urllib.parse.urlparse(sso_path)
    existing_params = dict(urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True))

    # Add/overwrite the uid and redirect_url parameters
    existing_params.update({
        "uid": uid,
        "redirect_uri": redirect_url,  # use a descriptive key
    })

    # Rebuild the query string
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # Construct the final URL
    final_url = urllib.parse.urlunparse((
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        new_query,
        parsed_sso.fragment
    ))

    return final_url