import urllib.parse
from typing import Set

# Example allowed domains; in real code this would be configured elsewhere.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Assemble a secure OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. 'https://app.example.com').
    callback_route : str
        The endpoint path that will handle the OAuth callback.
        Must start with '/' or be a relative path.
    token_state : str
        A unique state string used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in `ALLOWED_CALLBACK_DOMAINS`
        and does not match the application URL's domain.
    """
    # Parse the base application URL
    app_parsed = urllib.parse.urlparse(application_url)
    if not app_parsed.scheme or not app_parsed.netloc:
        raise ValueError(f"Invalid application URL: {application_url!r}")

    # Ensure callback_route is a relative path
    if not callback_route.startswith("/"):
        callback_route = "/" + callback_route

    # Join the base URL with the callback route
    joined_url = urllib.parse.urljoin(application_url.rstrip("/") + "/", callback_route.lstrip("/"))

    # Parse the joined URL to inspect its components
    callback_parsed = urllib.parse.urlparse(joined_url)

    # Validate the domain
    host = callback_parsed.hostname
    if not host:
        raise ValueError(f"Callback URL does not contain a valid hostname: {joined_url!r}")

    # Check against allowed domains or same domain as application
    if host not in ALLOWED_CALLBACK_DOMAINS and host != app_parsed.hostname:
        raise ValueError(
            f"Callback domain {host!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state query parameter safely
    query_params = urllib.parse.parse_qs(callback_parsed.query)
    # Keep existing parameters but override/append state
    query_params["state"] = [token_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL
    callback_url = urllib.parse.urlunparse(
        (
            callback_parsed.scheme,
            callback_parsed.netloc,
            callback_parsed.path,
            callback_parsed.params,
            new_query,
            callback_parsed.fragment,
        )
    )

    return callback_url