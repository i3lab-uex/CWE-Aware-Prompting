import urllib.parse
from typing import Iterable

# Domains that are permitted to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "myapp.example.org",
    # Add more trusted domains here.
}


def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str,
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The main base URL of the application (e.g., "https://myapp.example.org").
    callback_endpoint : str
        The path where the OAuth provider should redirect after authentication
        (e.g., "/auth/callback").
    verification_state : str
        A unique value to protect against CSRF attacks.

    Returns
    -------
    str
        The fully qualified OAuth callback URL with the state parameter appended.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the base URL ends with a slash so that urljoin behaves predictably
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Resolve the full callback URL
    resolved_callback = urllib.parse.urljoin(base, callback_endpoint)

    # Append the state parameter safely
    parsed = urllib.parse.urlparse(resolved_callback)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = verification_state
    new_query = urllib.parse.urlencode(query_params)

    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Validate domain against allowed list
    domain = urllib.parse.urlparse(final_url).hostname
    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {domain!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return final_url