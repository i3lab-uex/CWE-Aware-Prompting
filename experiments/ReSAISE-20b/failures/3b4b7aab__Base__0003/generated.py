import urllib.parse
from typing import Iterable, Set

# Example set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    "localhost",   # for local testing
}

def construct_oauth_callback_uri(
    root_url: str,
    callback_uri: str,
    session_state: str
) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g., "https://myapp.com").
    callback_uri : str
        The path component for the OAuth callback (e.g., "/auth/callback").
    session_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The complete callback URL with an appended `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the root URL is parsed correctly
    base = urllib.parse.urlparse(root_url)
    if not base.scheme or not base.netloc:
        raise ValueError(f"Invalid root URL: {root_url!r}")

    # Join the base URL with the callback path
    joined = urllib.parse.urljoin(base.geturl(), callback_uri)

    # Parse the resulting URL to manipulate query parameters
    parsed = urllib.parse.urlparse(joined)

    # Validate the domain against allowed domains
    hostname = parsed.hostname or ""
    if hostname.lower() not in (d.lower() for d in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Disallowed callback domain: {hostname!r}")

    # Append the state parameter
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_state]
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=encoded_query)
    )

    return final_url