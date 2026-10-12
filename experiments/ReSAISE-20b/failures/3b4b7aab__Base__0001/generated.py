import urllib.parse
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse

# Domains that are permitted for OAuth callback URLs
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add additional trusted domains here
}

def construct_oauth_callback_uri(root_url: str, callback_uri: str, session_state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (must include scheme and netloc).
    callback_uri : str
        Path or relative URL for the OAuth callback endpoint.
    session_state : str
        Unique value to include as a state parameter for CSRF protection.

    Returns
    -------
    str
        A fully qualified callback URL with the state parameter appended.

    Raises
    ------
    ValueError
        If `root_url` is malformed or the resulting callback domain is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Validate the base URL
    parsed_root = urlparse(root_url)
    if not (parsed_root.scheme and parsed_root.netloc):
        raise ValueError(f"Invalid root_url: {root_url!r}")

    # Resolve the callback path against the base URL
    joined = urljoin(root_url, callback_uri)
    parsed_joined = urlparse(joined)

    # Ensure the resulting domain is trusted
    if parsed_joined.netloc not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{parsed_joined.netloc}' is not allowed"
        )

    # Append the state parameter safely
    query_params = parse_qs(parsed_joined.query)
    query_params["state"] = [session_state]
    encoded_query = urlencode(query_params, doseq=True)

    # Rebuild the final URL
    final_url = urlunparse(
        (
            parsed_joined.scheme,
            parsed_joined.netloc,
            parsed_joined.path,
            parsed_joined.params,
            encoded_query,
            parsed_joined.fragment,
        )
    )

    return final_url