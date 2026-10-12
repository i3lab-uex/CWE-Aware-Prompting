import urllib.parse
from typing import Iterable

# Example allowed domains; in a real application this should be configured securely.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {"example.com", "auth.example.org"}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a safe OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_endpoint : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    verification_state : str
        A unique state value used for CSRF protection.

    Returns
    -------
    str
        The fully qualified callback URL with the state query parameter appended.

    Raises
    ------
    ValueError
        If the resolved callback URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Parse the base URL to ensure it is absolute and to extract its components.
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {app_base_url!r}")

    # Normalise the callback endpoint to avoid double slashes or missing leading slash.
    normalized_endpoint = callback_endpoint
    if not normalized_endpoint.startswith("/"):
        normalized_endpoint = "/" + normalized_endpoint

    # Resolve the full URL by combining base and endpoint.
    combined_path = urllib.parse.urljoin(parsed_base.path, normalized_endpoint)
    # Build the full URL with query parameters.
    query = urllib.parse.urlencode({"state": verification_state})
    callback_url_parts = (
        parsed_base.scheme,
        parsed_base.netloc,
        combined_path,
        "",  # params
        query,
        ""   # fragment
    )
    callback_url = urllib.parse.urlunparse(callback_url_parts)

    # Validate the domain of the resulting URL.
    callback_netloc = urllib.parse.urlparse(callback_url).netloc
    # Strip port if present for domain comparison.
    host = callback_netloc.split(":")[0]
    if host.lower() not in (d.lower() for d in ALLOWED_CALLBACK_DOMAINS):
        raise ValueError(f"Callback domain '{host}' is not allowed")

    return callback_url