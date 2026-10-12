import urllib.parse

# Example allowed domains – replace with your actual list.
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def build_sso_redirect_link(sso_service_url: str,
                            user_identifier: str,
                            redirect_back_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the third‑party SSO service (e.g. "https://sso.provider.com/login").
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_back_url : str
        URL to which the user should be returned after authentication.

    Returns
    -------
    str
        A fully‑qualified URL that the client can use to initiate SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL domain
    parsed_back = urllib.parse.urlparse(redirect_back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("redirect_back_url must be a valid absolute URL")

    # Extract the domain (netloc) and check against allowed list
    domain = parsed_back.hostname
    if not domain or domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build the query parameters
    params = {
        "user_id": user_identifier,
        "return_url": redirect_back_url,
    }
    encoded_params = urllib.parse.urlencode(params, safe=":/?&")

    # Combine with the SSO service base URL
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    # Preserve any existing query parameters in the SSO service URL
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # Merge with new params (new params override existing keys if duplicates)
    merged_params = {**{k: v[0] for k, v in existing_params.items()}, **params}
    final_query = urllib.parse.urlencode(merged_params, safe=":/?&")

    # Reconstruct the full URL
    final_parts = parsed_sso._replace(query=final_query)
    return urllib.parse.urlunparse(final_parts)

# Example usage:
if __name__ == "__main__":
    try:
        link = build_sso_redirect_link(
            sso_service_url="https://sso.provider.com/login",
            user_identifier="user-12345",
            redirect_back_url="https://example.com/dashboard"
        )
        print(link)
    except ValueError as e:
        print(f"Error: {e}")