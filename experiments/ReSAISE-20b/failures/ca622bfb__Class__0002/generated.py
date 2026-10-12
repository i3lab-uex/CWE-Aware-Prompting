import urllib.parse
from typing import Set

# Domains that are allowed to be used as callback URLs.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add more trusted domains here.
}


def assemble_oauth_callback_url(
    root_url: str, path_for_callback: str, session_token: str
) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_for_callback : str
        The endpoint that will receive the OAuth callback (e.g., "/oauth/callback").
    session_token : str
        A state token used to mitigate CSRF attacks.

    Returns
    -------
    str
        The complete callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL points to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS`` or if the URL cannot be parsed.
    """
    # Ensure path starts with a slash for correct joining.
    if not path_for_callback.startswith("/"):
        path_for_callback = "/" + path_for_callback

    # Join the root URL and callback path.
    joined_url = urllib.parse.urljoin(root_url.rstrip("/") + "/", path_for_callback.lstrip("/"))

    # Parse the joined URL to inspect its components.
    parsed = urllib.parse.urlparse(joined_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL constructed: {joined_url}")

    # Verify that the domain is allowed.
    host = parsed.hostname
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Domain '{host}' is not authorized for OAuth callbacks.")

    # Append the state query parameter safely.
    query = urllib.parse.urlencode({"state": session_token})
    callback_url = urllib.parse.urlunparse(
        parsed._replace(query=query)
    )

    return callback_url