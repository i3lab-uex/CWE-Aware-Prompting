import urllib.parse
from typing import Iterable

# Example allowed domains; replace with real values as needed.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {
    "example.com",
    "auth.example.org",
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_endpoint : str
        The path for the OAuth callback (e.g., "/oauth/callback").
    verification_state : str
        A unique state value used to prevent CSRF attacks.

    Returns
    -------
    str
        The fully-qualified OAuth callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Ensure base URL ends with a slash for correct joining
    base = app_base_url.rstrip("/") + "/"

    # Join the callback endpoint to the base URL
    full_path = urllib.parse.urljoin(base, callback_endpoint.lstrip("/"))

    # Parse the URL to inspect its components
    parsed = urllib.parse.urlparse(full_path)

    # Validate domain against the allowed list (case-insensitive)
    hostname = parsed.hostname
    if not hostname or hostname.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Disallowed callback domain: {hostname}")

    # Append the state parameter securely
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [verification_state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the URL with the new query string
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url