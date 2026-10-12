import urllib.parse
from typing import Set

# Example set of allowed callback domains. In a real application this would be
# populated from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str
) -> str:
    """
    Construct a secure OAuth redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The endpoint path for the OAuth callback handler (e.g., "/oauth/callback").
    session_state : str
        A unique identifier for the OAuth exchange (used as a CSRF protection token).

    Returns
    -------
    str
        The fully assembled OAuth callback URL.

    Raises
    ------
    ValueError
        If the resolved redirect URL's domain is not in ALLOWED_CALLBACK_DOMAINS and
        does not match the domain of ``main_url``.
    """
    if not all(isinstance(arg, str) for arg in (main_url, redirect_endpoint, session_state)):
        raise TypeError("All arguments must be strings")

    # Resolve the full callback URL
    # urljoin handles relative paths correctly
    full_url = urllib.parse.urljoin(main_url.rstrip('/') + '/', redirect_endpoint.lstrip('/'))

    # Parse the URL to extract components
    parsed = urllib.parse.urlparse(full_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid redirect URL: {full_url}")

    # Validate domain
    callback_domain = parsed.hostname.lower() if parsed.hostname else ""
    main_domain = urllib.parse.urlparse(main_url).hostname.lower()

    # The domain is considered valid if it matches the main domain or
    # is explicitly listed in ALLOWED_CALLBACK_DOMAINS.
    if callback_domain != main_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter
    query = urllib.parse.urlencode({"state": session_state})
    callback_url = parsed._replace(query=query).geturl()

    return callback_url