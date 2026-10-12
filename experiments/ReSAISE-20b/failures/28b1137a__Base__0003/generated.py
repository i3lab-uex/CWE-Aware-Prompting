import urllib.parse

# Whitelisted domains for the redirect URL (example values)
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "trusted.example.org",
    "app.company.net",
}

def _extract_domain(url: str) -> str:
    """
    Extracts the hostname from a URL, stripping any port.
    Raises ValueError if the URL is malformed or has no hostname.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")
    # Remove port if present
    host = parsed.hostname or ""
    return host.lower()

def build_sso_url(sso_path: str, uid: str, redirect_url: str) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_path : str
        Base URL of the SSO endpoint.
    uid : str
        User identifier to be passed as a query parameter.
    redirect_url : str
        Destination URL after successful SSO. Must belong to a whitelisted domain.

    Returns
    -------
    str
        Fully constructed SSO URL with query parameters encoded.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the redirect URL's domain
    host = _extract_domain(redirect_url)
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Redirect domain {host!r} is not allowed")

    # Parse the SSO endpoint to manipulate its query string
    parsed_sso = urllib.parse.urlparse(sso_path)

    # Existing query parameters (if any)
    existing_qs = urllib.parse.parse_qsl(parsed_sso.query, keep_blank_values=True)

    # Append our parameters
    new_params = existing_qs + [
        ("uid", uid),
        ("redirect_url", redirect_url),
    ]

    # Reconstruct the full URL
    new_query = urllib.parse.urlencode(new_params, doseq=True)

    sso_url_parts = parsed_sso._replace(query=new_query)
    return urllib.parse.urlunparse(sso_url_parts)


# Example usage
if __name__ == "__main__":
    try:
        url = build_sso_url(
            sso_path="https://sso.example.com/login",
            uid="user123",
            redirect_url="https://app.company.net/dashboard"
        )
        print(url)
    except ValueError as exc:
        print(f"Error: {exc}")