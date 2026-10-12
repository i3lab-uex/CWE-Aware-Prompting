import urllib.parse
from typing import Set

# Example set of allowed callback domains. In real usage this should be configured
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "api.example.com"}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Assemble a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g., "https://myapp.com").
    callback_route : str
        The path to the OAuth callback handler (e.g., "/auth/callback").
    token_state : str
        A unique state value to protect against CSRF attacks.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS or
        does not match the application domain.
    """
    # Normalize the base URL and ensure it ends with a slash for urljoin
    base = application_url.rstrip('/') + '/'
    # Join the callback route to the base URL
    raw_callback = urllib.parse.urljoin(base, callback_route.lstrip('/'))

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(raw_callback)

    # Validate scheme: only http and https are acceptable
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate host
    host = parsed.hostname
    if not host:
        raise ValueError("Callback URL must contain a hostname")

    # Ensure the callback domain is either the same as the application or in allowed list
    app_parsed = urllib.parse.urlparse(application_url)
    if host != app_parsed.hostname and host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {host}")

    # Build query parameters, preserving existing ones
    query_params = urllib.parse.parse_qs(parsed.query)
    # Add or replace the state parameter
    query_params["state"] = [token_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL
    assembled = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return assembled