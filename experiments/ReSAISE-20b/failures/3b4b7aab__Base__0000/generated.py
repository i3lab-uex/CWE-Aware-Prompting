import urllib.parse
from typing import Iterable, Sequence

# Define a set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Sequence[str] = [
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
]


def construct_oauth_callback_uri(
    root_url: str,
    callback_uri: str,
    session_state: str,
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_uri : str
        The path to the OAuth callback endpoint (e.g., "/auth/callback").
    session_state : str
        A unique value to include as the `state` query parameter.

    Returns
    -------
    str
        A fully qualified callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the computed callback URL's domain is not in `ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the full callback URL relative to the root
    base_parsed = urllib.parse.urlparse(root_url)
    # Ensure callback_uri is a path (not an absolute URL)
    if urllib.parse.urlparse(callback_uri).scheme:
        raise ValueError("callback_uri must be a relative path, not an absolute URL")

    # Join root and callback path
    full_path = urllib.parse.urljoin(base_parsed.geturl(), callback_uri)

    # Parse the joined URL to inspect its components
    parsed = urllib.parse.urlparse(full_path)

    # Validate domain against allowed list (case‑insensitive)
    hostname = parsed.hostname or ""
    if hostname.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Disallowed callback domain: {hostname}")

    # Append the state parameter safely
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [session_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Rebuild the URL with the updated query string
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return safe_url