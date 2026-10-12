import urllib.parse
from typing import Iterable

# Example set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {
    "example.com",
    "auth.example.org",
    "localhost",  # for local testing
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str,
) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. ``https://app.example.com``).
    callback_endpoint : str
        The path segment that receives the OAuth redirect (e.g. ``/oauth/callback``).
    verification_state : str
        A unique value that will be added as a query parameter to verify the request.

    Returns
    -------
    str
        The complete callback URL, including scheme, host and query string.

    Raises
    ------
    ValueError
        If the resulting URL's host is not in :data:`ALLOWED_CALLBACK_DOMAINS`.

    Notes
    -----
    The function uses :func:`urllib.parse.urljoin` to combine the base URL and
    callback endpoint safely, then validates that the host is in the allowed list.
    It also ensures that a ``state`` query parameter is added for security
    verification, preventing CSRF attacks.  This implementation mitigates
    CWE‑601 (Open Redirect) by rejecting any callback URL that points to an
    untrusted domain.
    """
    # Parse the base URL and ensure it contains a scheme and netloc
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must include a valid scheme and host")

    # Join the base URL with the callback endpoint
    joined_url = urllib.parse.urljoin(app_base_url, callback_endpoint)

    # Parse the joined URL to extract components
    parsed_joined = urllib.parse.urlparse(joined_url)

    # Validate the domain against allowed list (case‑insensitive)
    host = parsed_joined.hostname or ""
    if host.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Callback domain '{host}' is not allowed")

    # Build query parameters, preserving any existing ones
    query_params = urllib.parse.parse_qs(parsed_joined.query)
    # `parse_qs` returns values as lists; we flatten for a single value
    query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
    query_params["state"] = verification_state

    # Reconstruct the URL with the updated query string
    final_url_parts = (
        parsed_joined.scheme,
        parsed_joined.netloc,
        parsed_joined.path,
        parsed_joined.params,
        urllib.parse.urlencode(query_params, doseq=True),
        parsed_joined.fragment,
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url