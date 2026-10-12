import urllib.parse

# Example allowed domains; in real code this would come from config.
ALLOWED_RETURN_DOMAINS = {"example.com", "trustedsite.org"}


def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (must be absolute).
    user_identifier : str
        Unique identifier for the user.
    redirect_back_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the return URL to validate its domain.
    parsed_back = urllib.parse.urlparse(redirect_back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("redirect_back_url must be an absolute URL")

    # Extract the domain (hostname) and compare to allowed list.
    hostname = parsed_back.hostname
    if not hostname or hostname.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain '{hostname}' is not allowed. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # Build query parameters for the SSO service.
    params = {
        "user": user_identifier,
        # The redirect URL must be URL‑encoded to preserve its query string.
        "redirect": redirect_back_url,
    }
    encoded_params = urllib.parse.urlencode(params, safe="/:?&=")

    # Construct the final redirect URL.
    base = urllib.parse.urlparse(sso_service_url)
    if not base.scheme or not base.netloc:
        raise ValueError("sso_service_url must be an absolute URL")

    # Append the query string to the SSO service base URL.
    sso_url = urllib.parse.urlunparse(
        (
            base.scheme,
            base.netloc,
            base.path,
            base.params,
            encoded_params,
            base.fragment,
        )
    )

    return sso_url