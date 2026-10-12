import urllib.parse
from typing import Set

# Example set of allowed callback domains. In real usage this should be
# configured securely and never hard‑coded.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://app.example.com").
    redirect_endpoint : str
        The path or endpoint that handles the OAuth callback.
        It may be a relative path ("/oauth/callback") or an absolute URL.
    session_state : str
        A unique identifier that ties the request to a user session.

    Returns
    -------
    str
        A fully qualified URL that can be used as the OAuth redirect URI.

    Raises
    ------
    ValueError
        If the resulting callback URL points to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS`` and does not match the host of
        ``main_url``.
    """
    # Parse the main URL to extract its scheme and host
    try:
        parsed_main = urllib.parse.urlparse(main_url)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid main_url '{main_url}': {exc}") from exc

    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"main_url must be a valid absolute URL: {main_url}")

    # Build the full callback URL
    # urljoin handles relative paths and absolute URLs correctly.
    raw_callback = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Parse the resulting callback URL to inspect its domain
    parsed_callback = urllib.parse.urlparse(raw_callback)

    # Ensure the callback URL is absolute
    if not parsed_callback.scheme or not parsed_callback.netloc:
        raise ValueError(f"Callback URL is not absolute: {raw_callback}")

    # Normalise the host for comparison (lowercase, strip port if present)
    def normalise_host(host: str) -> str:
        return host.split(":")[0].lower()

    callback_host = normalise_host(parsed_callback.netloc)
    main_host = normalise_host(parsed_main.netloc)

    # Security check: callback must be either the same host as main_url
    # or belong to an explicitly allowed domain.
    if callback_host != main_host and callback_host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the session state as a query parameter. Preserve existing
    # query parameters if any.
    query = urllib.parse.parse_qs(parsed_callback.query, keep_blank_values=True)
    # parse_qs returns lists for each key; we want a single value.
    query["state"] = [session_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the final URL
    final_parts = parsed_callback._replace(query=new_query)
    return urllib.parse.urlunparse(final_parts)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    url = build_oauth_redirect_url(
        main_url="https://app.example.com",
        redirect_endpoint="/oauth/callback",
        session_state="abc123"
    )
    print(url)