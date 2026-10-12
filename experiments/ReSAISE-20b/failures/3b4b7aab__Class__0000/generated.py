import urllib.parse
from typing import Iterable

# Example list of allowed callback domains; in real usage this would be a config
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}


def construct_oauth_callback_uri(
    root_url: str, callback_uri: str, session_state: str
) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_uri : str
        The relative or absolute path to the OAuth callback endpoint
        (e.g. "/auth/callback").
    session_state : str
        A unique token that will be appended as the `state` query parameter.

    Returns
    -------
    str
        The final callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the full URL; if callback_uri is already absolute it will override root_url
    base = urllib.parse.urljoin(root_url, callback_uri)

    # Append the state parameter safely
    parsed = urllib.parse.urlparse(base)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the URL with updated query
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Validate the domain
    domain = urllib.parse.urlparse(final_url).hostname
    if not domain or domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Disallowed callback domain: {domain!r}")

    return final_url