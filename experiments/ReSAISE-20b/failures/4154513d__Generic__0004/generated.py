import urllib.parse

# Domains that are permitted for the redirect URL.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base SSO service endpoint.
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The complete redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the domain of ``redirect_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect URL domain
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError("Invalid redirect URL")

    # Extract hostname (without port) for domain comparison
    hostname = parsed_redirect.hostname.lower()
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain '{hostname}' is not allowed")

    # Prepare query parameters, ensuring proper encoding
    query_params = urllib.parse.urlencode(
        {"uid": uid, "redirect": redirect_url}
    )

    # Append the query to the auth endpoint
    if urllib.parse.urlparse(auth_endpoint).query:
        # If auth_endpoint already contains query parameters, merge them
        base, existing_query = urllib.parse.splitquery(auth_endpoint)
        combined_query = f"{existing_query}&{query_params}"
        final_url = urllib.parse.urlunparse(
            (*urllib.parse.urlparse(base), combined_query, "")
        )
    else:
        delimiter = "?" if "?" not in auth_endpoint else "&"
        final_url = f"{auth_endpoint}{delimiter}{query_params}"

    return final_url