import urllib.parse

# Domains that are allowed for the redirect_back_url parameter.
ALLOWED_RETURN_DOMAINS = {"example.com", "trusted.example.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g. "https://sso.example.com/login").
    user_identifier : str
        Unique identifier for the user (e.g. a UUID or username).
    redirect_back_url : str
        URL to return to after successful SSO. Must belong to an allowed domain.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the redirect_back_url to extract its domain
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("redirect_back_url must be a full, absolute URL")

    # Normalize the domain (lowercase) and strip port if present
    domain = parsed_return.netloc.split(":")[0].lower()

    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{domain}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters for the SSO service
    query_params = {
        "user_id": user_identifier,
        # Ensure the return URL is safely percent-encoded
        "return_url": redirect_back_url,
    }

    # Construct the final SSO URL
    sso_parsed = urllib.parse.urlparse(sso_service_url)
    # Merge existing query params with new ones
    existing_params = dict(urllib.parse.parse_qsl(sso_parsed.query))
    merged_params = {**existing_params, **query_params}
    encoded_query = urllib.parse.urlencode(merged_params)

    final_url_parts = sso_parsed._replace(query=encoded_query)
    return urllib.parse.urlunparse(final_url_parts)


# Example usage:
if __name__ == "__main__":
    sso_base = "https://sso.example.com/login"
    user_id = "user-12345"
    back_url = "https://trusted.example.org/dashboard"

    try:
        redirect_link = build_sso_redirect_link(sso_base, user_id, back_url)
        print("SSO Redirect URL:", redirect_link)
    except ValueError as e:
        print("Invalid return URL:", e)