import urllib.parse
from typing import Set

# Domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "api.example.com",
    # Add more domains as needed
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g. "https://myapp.com").
    callback_path : str
        The path where the OAuth provider will redirect back (e.g. "/auth/callback").
    state : str
        A unique opaque value to prevent CSRF attacks.

    Returns
    -------
    str
        The fully-qualified callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL is parsed correctly
    parsed_base = urllib.parse.urlparse(base_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")

    # Build the path part, ensuring no double slashes
    callback_path = "/" + callback_path.lstrip("/")
    # Combine the base URL with the callback path
    combined = urllib.parse.urljoin(parsed_base.geturl(), callback_path)

    # Append the state query parameter
    url_parts = list(urllib.parse.urlparse(combined))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query["state"] = state
    url_parts[4] = urllib.parse.urlencode(query)
    final_url = urllib.parse.urlunparse(url_parts)

    # Validate that the domain is allowed
    final_netloc = urllib.parse.urlparse(final_url).netloc.lower()
    # Extract the domain part (exclude port if present)
    domain = final_netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain!r}")

    return final_url