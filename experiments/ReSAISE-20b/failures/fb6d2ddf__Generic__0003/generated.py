import urllib.parse

# Whitelist of domains allowed for the redirect URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    "trusted-site.net",
}

def _extract_domain(url: str) -> str:
    """
    Extract the hostname (domain) from a URL, excluding any port.
    """
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    return hostname.lower()

def create_sso_url(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO provider.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the user should be sent after authentication.

    Returns
    -------
    str
        The fully-formed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain
    domain = _extract_domain(redirect_url)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect URL domain '{domain}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Parse the auth endpoint
    parsed_auth = urllib.parse.urlparse(auth_endpoint)

    # Merge existing query parameters with the new ones
    existing_params = urllib.parse.parse_qs(parsed_auth.query, keep_blank_values=True)
    # parse_qs returns lists for each key; convert to single values
    params = {k: v[0] if len(v) == 1 else v for k, v in existing_params.items()}

    # Add/overwrite the required parameters
    params["uid"] = uid
    params["redirect_url"] = redirect_url

    # Reconstruct the query string
    new_query = urllib.parse.urlencode(params, doseq=True)

    # Build the final URL
    new_url = urllib.parse.urlunparse(
        parsed_auth._replace(query=new_query)
    )
    return new_url