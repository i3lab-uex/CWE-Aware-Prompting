import urllib.parse

# Allowed domains for the redirect back URL (example set)
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.org"}

def build_sso_redirect_link(sso_service_url: str,
                            user_identifier: str,
                            redirect_back_url: str) -> str:
    """
    Construct a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (may contain existing query parameters).
    user_identifier : str
        Unique identifier of the user to be sent to the SSO service.
    redirect_back_url : str
        URL that the SSO provider should redirect to after authentication.

    Returns
    -------
    str
        The fully‑formed SSO redirect URL containing the user identifier and
        a safe return URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Validate the return URL domain
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("redirect_back_url must be a fully-qualified URL")

    # Extract the domain (hostname) and normalize it
    hostname = parsed_return.hostname.lower()
    if hostname not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return domain '{hostname}' is not allowed")

    # Build query parameters
    params = {
        "user_id": user_identifier,
        "redirect_back": redirect_back_url
    }

    # Parse the base SSO service URL to preserve existing query params
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    # Merge existing query parameters with new ones
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # parse_qs returns lists; flatten for simplicity
    merged_params = {k: v[0] if len(v) == 1 else v for k, v in existing_params.items()}
    merged_params.update(params)

    # Reconstruct the URL
    new_query = urllib.parse.urlencode(merged_params, doseq=True)
    new_parts = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(new_parts)

# Example usage (for testing only, remove or comment out in production)
if __name__ == "__main__":
    sso_url = "https://sso.example.com/auth"
    user_id = "alice123"
    back_url = "https://example.com/dashboard"

    redirect_link = build_sso_redirect_link(sso_url, user_id, back_url)
    print(redirect_link)