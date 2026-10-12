import urllib.parse

# Domains that are allowed to receive the redirect back.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
}

def _extract_domain(netloc: str) -> str:
    """
    Extract the host part of a netloc, stripping any port.
    """
    return netloc.split(":")[0].lower()


def _is_allowed_domain(domain: str) -> bool:
    """
    Check that the domain is in ALLOWED_RETURN_DOMAINS.
    Only exact matches are accepted to avoid sub‑domain confusion (CWE‑610).
    """
    return domain in ALLOWED_RETURN_DOMAINS


def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a single sign‑on redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO service (e.g., "https://sso.example.com/auth").
    user_identifier : str
        Unique identifier for the user (e.g., a UUID or username).
    redirect_back_url : str
        URL to which the SSO provider should redirect after authentication.

    Returns
    -------
    str
        The fully constructed SSO redirect URL with query parameters encoded.

    Raises
    ------
    ValueError
        If the domain of `redirect_back_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the return URL
    parsed_back = urllib.parse.urlparse(redirect_back_url)
    if not parsed_back.scheme or not parsed_back.netloc:
        raise ValueError("redirect_back_url must be a fully qualified URL")

    domain = _extract_domain(parsed_back.netloc)
    if not _is_allowed_domain(domain):
        raise ValueError(
            f"Return URL domain '{domain}' is not permitted. "
            "Allowed domains: " + ", ".join(sorted(ALLOWED_RETURN_DOMAINS))
        )

    # Build the query parameters
    params = {
        "user": user_identifier,
        "redirect_back": redirect_back_url,  # will be percent‑encoded by urlencode
    }
    query_string = urllib.parse.urlencode(params, safe="")

    # Ensure the base SSO URL does not already contain a query string
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    if parsed_sso.query:
        raise ValueError("sso_service_url must not contain a query string")

    # Construct the final URL
    sso_redirect = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            query_string,
            "",  # fragment
        )
    )

    return sso_redirect