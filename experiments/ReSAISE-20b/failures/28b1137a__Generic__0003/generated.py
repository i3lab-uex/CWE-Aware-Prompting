import urllib.parse

# Whitelist of domains that are allowed as return URLs.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "myapp.org",
    "trusted-site.net",
}

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        Base URL of the SSO endpoint (e.g. "https://sso.provider.com/auth").
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the identity provider should redirect after authentication.

    Returns
    -------
    str
        Fully qualified URL that the client can use to initiate SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect URL to extract its domain.
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("redirect_url must be a valid absolute URL")

    # Extract the hostname (e.g., "sub.example.com") and compare against the whitelist.
    hostname = parsed_redirect.hostname or ""
    # The host may contain subdomains; we allow any subdomain of a whitelisted domain.
    if not any(hostname == allowed or hostname.endswith("." + allowed)
               for allowed in ALLOWED_RETURN_DOMAINS):
        raise ValueError(f"redirect_url domain '{hostname}' is not allowed")

    # Build the query parameters.  We include the user ID and a URL‑encoded redirect URL.
    query_params = {
        "uid": uid,
        # The redirect URL must be percent‑encoded to preserve its query string.
        "redirect": redirect_url,
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Combine the base SSO path with the query string.
    # Ensure that we don't duplicate a '?' if sso_path already contains one.
    separator = "&" if "?" in sso_path else "?"
    full_url = f"{sso_path}{separator}{encoded_query}"
    return full_url