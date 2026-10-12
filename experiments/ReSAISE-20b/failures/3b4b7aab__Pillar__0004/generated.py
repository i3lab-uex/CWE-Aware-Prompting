import urllib.parse
from typing import Iterable

# Example allowed domains – in real use these would be configured elsewhere.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}

def construct_oauth_callback_uri(
    root_url: str,
    callback_uri: str,
    session_state: str
) -> str:
    """
    Build a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The application's base URL (e.g., "https://app.example.com/").
    callback_uri : str
        The path for the OAuth callback (e.g., "/oauth/callback").
    session_state : str
        A unique value used to validate the OAuth flow.

    Returns
    -------
    str
        The fully‑qualified callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # 1. Ensure callback_uri is a relative path or an allowed absolute URL.
    parsed_callback = urllib.parse.urlparse(callback_uri)
    if parsed_callback.scheme:
        # Absolute URL – check its domain immediately.
        callback_netloc = parsed_callback.netloc.lower()
        if callback_netloc not in ALLOWED_CALLBACK_DOMAINS:
            raise ValueError(
                f"Callback URL domain '{callback_netloc}' is not allowed."
            )
        base_url = callback_uri
    else:
        # Relative path – safely join with root_url.
        base_url = urllib.parse.urljoin(root_url.rstrip('/') + '/', callback_uri.lstrip('/'))

    # 2. Append the state parameter securely.
    parsed_base = urllib.parse.urlparse(base_url)
    query_params = dict(urllib.parse.parse_qsl(parsed_base.query, keep_blank_values=True))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # 3. Reconstruct the full URL.
    final_url = urllib.parse.urlunparse(
        parsed_base._replace(query=new_query)
    )

    # 4. Validate the final domain.
    final_domain = urllib.parse.urlparse(final_url).netloc.lower()
    if final_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Final callback URL domain '{final_domain}' is not allowed."
        )

    return final_url