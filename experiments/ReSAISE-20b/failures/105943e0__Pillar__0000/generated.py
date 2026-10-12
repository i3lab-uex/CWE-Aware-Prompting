import urllib.parse

# Domains that are allowed to receive the user after SSO authentication.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "auth.example.org",
    "myapp.local"
}

def _is_allowed_domain(url: str) -> bool:
    """
    Check whether the domain of a URL is in ALLOWED_RETURN_DOMAINS.
    The comparison is case‑insensitive and ignores subdomains that are
    not explicitly listed.

    :param url: The URL to check.
    :return: True if the domain is allowed, False otherwise.
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    # Normalize to lower‑case
    host = host.lower()
    return host in ALLOWED_RETURN_DOMAINS

def create_sso_redirect_url(
        login_endpoint: str,
        account_id: str,
        callback_url: str
) -> str:
    """
    Build a redirect URL for SSO authentication.

    The resulting URL points to `login_endpoint` and contains the
    `account_id` and a URL‑encoded `callback_url`.  The callback URL's
    domain must be in the set of allowed domains; otherwise a
    ValueError is raised.

    :param login_endpoint: The SSO service endpoint URL.
    :param account_id:   Unique identifier for the user.
    :param callback_url: URL to which the user should be returned after
                         authentication.

    :returns: The full redirect URL for SSO.
    :raises ValueError: If `callback_url` contains a disallowed domain
                        or if either argument is not a valid absolute URL.
    """
    # Validate the login endpoint
    parsed_login = urllib.parse.urlparse(login_endpoint)
    if not parsed_login.scheme or not parsed_login.netloc:
        raise ValueError("login_endpoint must be an absolute URL")

    # Validate the callback URL
    parsed_callback = urllib.parse.urlparse(callback_url)
    if not parsed_callback.scheme or not parsed_callback.netloc:
        raise ValueError("callback_url must be an absolute URL")

    if not _is_allowed_domain(callback_url):
        raise ValueError(
            f"Return URL domain '{parsed_callback.hostname}' is not allowed"
        )

    # Build query parameters safely
    query_params = {
        "account_id": account_id,
        "return_url": callback_url
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Construct the final redirect URL
    return f"{login_endpoint.rstrip('/')}/{parsed_login.path.lstrip('/')}?{encoded_query}"