import urllib.parse

# Domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local"
}


def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a SSO redirect URL that points to the authentication endpoint
    and includes the user ID and a return URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO service endpoint (e.g. "https://sso.example.com/auth").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        The URL to return to after authentication.

    Returns
    -------
    str
        A fully‑formed redirect URL containing the required query parameters.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # 1. Validate the return URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    hostname = parsed_redirect.hostname
    if not hostname:
        raise ValueError("Invalid redirect URL: missing hostname")

    # Normalize hostname for comparison
    hostname = hostname.lower()

    # The URL is allowed if the hostname exactly matches or ends with an
    # allowed domain prefixed by a dot (to allow sub‑domains).
    if not any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in ALLOWED_RETURN_DOMAINS
    ):
        raise ValueError(
            f"Return URL domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # 2. Build the query string
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,
    }
    encoded_params = urllib.parse.urlencode(query_params, safe="/:")

    # 3. Combine the auth endpoint with the query string
    if urllib.parse.urlparse(auth_endpoint).scheme == "":
        # Ensure auth_endpoint is absolute; raise if not
        raise ValueError("auth_endpoint must be an absolute URL with scheme")

    # If auth_endpoint already contains a query string, merge it
    base_parts = urllib.parse.urlparse(auth_endpoint)
    existing_query = dict(urllib.parse.parse_qsl(base_parts.query))
    merged_query = {**existing_query, **query_params}
    new_query = urllib.parse.urlencode(merged_query, safe="/:")

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            base_parts.scheme,
            base_parts.netloc,
            base_parts.path,
            base_parts.params,
            new_query,
            base_parts.fragment,
        )
    )

    return final_url