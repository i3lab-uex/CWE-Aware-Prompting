import urllib.parse
from typing import Set

# Example allowed domains – replace with the real set used in your application.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g. "https://myapp.com").
    callback_route : str
        The endpoint for the OAuth callback handler. May be a relative path
        (e.g. "/auth/callback") or an absolute URL.
    token_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        A fully assembled, validated callback URL containing the state parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in `ALLOWED_CALLBACK_DOMAINS`
        and does not match the application host.
    """
    # Parse the base application URL
    app_parsed = urllib.parse.urlparse(application_url)
    if not (app_parsed.scheme and app_parsed.netloc):
        raise ValueError("`application_url` must be a valid absolute URL")

    # Resolve the callback route – treat as relative if it doesn't contain scheme
    if urllib.parse.urlparse(callback_route).scheme:
        # absolute URL supplied – use it directly
        callback_parsed = urllib.parse.urlparse(callback_route)
    else:
        # relative path – join with the base application URL
        joined = urllib.parse.urljoin(application_url.rstrip('/') + '/', callback_route.lstrip('/'))
        callback_parsed = urllib.parse.urlparse(joined)

    # Validate domain
    callback_host = callback_parsed.hostname
    if not callback_host:
        raise ValueError("Callback URL must have a valid host")

    # Allow same‑domain callbacks or those explicitly whitelisted
    app_host = app_parsed.hostname
    if callback_host != app_host and callback_host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter
    query_params = urllib.parse.parse_qs(callback_parsed.query, keep_blank_values=True)
    # parse_qs returns list values; convert to single value for state
    query_params["state"] = [token_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL
    assembled = urllib.parse.urlunparse(
        (
            callback_parsed.scheme,
            callback_parsed.netloc,
            callback_parsed.path,
            callback_parsed.params,
            new_query,
            callback_parsed.fragment,
        )
    )

    return assembled