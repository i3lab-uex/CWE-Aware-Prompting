import urllib.parse

# Whitelisted domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net",
}


def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        The base SSO endpoint URL (e.g. "https://auth.example.com/sso").
    uid : str
        The unique identifier of the user.
    redirect_url : str
        The URL to which the identity provider should return after login.

    Returns
    -------
    str
        The fully-qualified SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL and validate its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect URL: {redirect_url}")

    # Extract hostname (without port) for comparison.
    host = parsed_redirect.hostname or ""
    if host.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain '{host}' is not in the allowed list: {ALLOWED_RETURN_DOMAINS}"
        )

    # Parse the SSO endpoint and merge query parameters.
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Build new query dict with existing parameters (if any).
    sso_query = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # Flatten values: parse_qs returns lists; we want single values.
    flattened_sso_query = {k: v[0] for k, v in sso_query.items()}

    # Add/override uid and redirect_url parameters.
    flattened_sso_query.update(
        {
            "uid": uid,
            # Encode the redirect URL to preserve its structure.
            "redirect_url": redirect_url,
        }
    )

    # Reconstruct the full SSO URL.
    new_query = urllib.parse.urlencode(flattened_sso_query, doseq=False)
    sso_url_parts = (
        parsed_sso.scheme,
        parsed_sso.netloc,
        parsed_sso.path,
        parsed_sso.params,
        new_query,
        parsed_sso.fragment,
    )
    return urllib.parse.urlunparse(sso_url_parts)


# Example usage (for testing purposes):
if __name__ == "__main__":
    try:
        url = build_sso_url(
            sso_path="https://auth.example.com/sso",
            uid="user-12345",
            redirect_url="https://app.example.org/dashboard?view=home",
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")