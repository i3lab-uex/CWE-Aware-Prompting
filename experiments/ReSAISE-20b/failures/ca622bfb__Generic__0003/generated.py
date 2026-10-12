import urllib.parse
from typing import Set

# Domains that are permitted to be used as OAuth callback targets.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add any additional domains that are allowed here.
}

def assemble_oauth_callback_url(
    root_url: str,
    path_for_callback: str,
    session_token: str
) -> str:
    """
    Construct a full OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    path_for_callback : str
        The callback endpoint relative to the root URL (e.g. "/oauth/callback").
    session_token : str
        A token used as the OAuth state parameter.

    Returns
    -------
    str
        The fully-qualified callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL points to a domain not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the root URL has a scheme and netloc
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme or not parsed_root.netloc:
        raise ValueError(f"Invalid root URL: {root_url!r}")

    # Build the full callback path relative to the root
    callback_path = urllib.parse.urljoin(parsed_root.path + "/", path_for_callback.lstrip("/"))

    # Construct the full URL without query
    base_url = urllib.parse.urlunparse((
        parsed_root.scheme,
        parsed_root.netloc,
        callback_path,
        "",  # params
        "",  # query (will be added next)
        ""   # fragment
    ))

    # Append the state parameter securely
    query = urllib.parse.urlencode({"state": session_token})
    full_url = f"{base_url}?{query}"

    # Validate the domain of the final URL
    parsed_full = urllib.parse.urlparse(full_url)
    if parsed_full.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {parsed_full.netloc!r}")

    return full_url