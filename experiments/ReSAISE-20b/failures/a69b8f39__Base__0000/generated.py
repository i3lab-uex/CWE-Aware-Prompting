import urllib.parse

# Example allowed domains – replace with your actual list.
ALLOWED_RETURN_DOMAINS = {"example.com", "myapp.org"}


def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service : str
        Base URL of the SSO service.
    user_ref : str
        Unique identifier for the user.
    back_url : str
        URL to return to after SSO. Must be absolute and belong to an allowed domain.

    Returns
    -------
    str
        Full SSO redirect URL with user_ref and return_url encoded.

    Raises
    ------
    ValueError
        If ``back_url`` is not absolute or its domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the return URL
    parsed_back = urllib.parse.urlparse(back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("back_url must be an absolute URL")

    # Normalize domain (ignore port)
    domain = parsed_back.netloc.split(":")[0]
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Parse the SSO service URL to preserve any existing query parameters
    sso_parsed = urllib.parse.urlparse(sso_service)

    # Build the query dict, preserving existing params
    existing_params = urllib.parse.parse_qs(sso_parsed.query, keep_blank_values=True)
    # Add/override with our parameters
    existing_params.update(
        {
            "user_ref": [user_ref],
            # Use the raw back_url; it will be URL‑encoded by urlencode
            "return_url": [back_url],
        }
    )

    # Reconstruct the full URL
    new_query = urllib.parse.urlencode(existing_params, doseq=True)
    sso_url_parts = list(sso_parsed)
    sso_url_parts[4] = new_query  # index 4 is the query component
    final_url = urllib.parse.urlunparse(sso_url_parts)

    return final_url