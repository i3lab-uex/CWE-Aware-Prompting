import urllib.parse
from typing import Set

# Allowed domains for OAuth callback URLs.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add other trusted domains here
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    base_url : str
        Base URL of the application (e.g. "https://myapp.com").
    callback_path : str
        Path to the OAuth callback endpoint (e.g. "/auth/callback").
    state : str
        Unique state string to mitigate CSRF attacks.

    Returns
    -------
    str
        A fully qualified callback URL with the `state` query parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain in
        ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Join the base URL with the callback path. ``urljoin`` handles
    # missing slashes and normalizes the result.
    joined_url = urllib.parse.urljoin(base_url.rstrip("/") + "/", callback_path.lstrip("/"))

    # Parse the URL components
    parsed = urllib.parse.urlparse(joined_url)

    # Extract hostname (strip any port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Callback URL must contain a valid hostname")

    # Ensure the domain is allowed
    if hostname.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Domain '{hostname}' is not allowed for OAuth callbacks")

    # Build query parameters: preserve existing ones, add/overwrite `state`
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    # parse_qs returns lists; we want a single value for state
    query_params["state"] = [state]
    # Reconstruct the query string
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reassemble the full URL with the new query string
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    return final_url