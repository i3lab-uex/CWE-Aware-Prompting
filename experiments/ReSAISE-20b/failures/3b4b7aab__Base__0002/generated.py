import urllib.parse
from typing import Iterable

# Example set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add any other domains that are trusted for OAuth callbacks.
}

def _extract_domain(netloc: str) -> str:
    """
    Return the hostname part of a netloc, stripping any port.
    """
    return netloc.split(":")[0].lower()

def construct_oauth_callback_uri(
    root_url: str,
    callback_uri: str,
    session_state: str
) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's main base URL (e.g., "https://app.example.com").
    callback_uri : str
        The path or relative URL for the OAuth callback endpoint (e.g., "/oauth/callback").
    session_state : str
        A unique value to include as the `state` query parameter for CSRF protection.

    Returns
    -------
    str
        The complete callback URL with the `state` parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Normalise and join the base URL with the callback path
    joined_url = urllib.parse.urljoin(root_url.rstrip("/") + "/", callback_uri.lstrip("/"))

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(joined_url)

    # Ensure the URL is absolute (has a scheme)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Callback URL must be absolute and contain a network location")

    # Validate the domain against the allowed list
    domain = _extract_domain(parsed.netloc)
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Disallowed callback domain: {domain!r}")

    # Append the state query parameter
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = session_state
    encoded_query = urllib.parse.urlencode(query_params)

    # Rebuild the URL with the updated query string
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            encoded_query,
            parsed.fragment,
        )
    )

    return final_url