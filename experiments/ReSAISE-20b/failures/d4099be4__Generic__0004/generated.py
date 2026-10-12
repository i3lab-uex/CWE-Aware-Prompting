import urllib.parse
from typing import Iterable, Set

# Domains that are allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add additional trusted domains here.
}

def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_endpoint : str
        The path that will handle the OAuth callback (e.g. "/auth/oauth/callback").
    verification_state : str
        A unique token that will be appended as the `state` query parameter.

    Returns
    -------
    str
        A safe, fully‑qualified callback URL that includes the `state` parameter.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the callback endpoint starts with a slash.
    if not callback_endpoint.startswith("/"):
        callback_endpoint = "/" + callback_endpoint

    # Join the base URL with the endpoint to get a full path.
    raw_url = urllib.parse.urljoin(app_base_url, callback_endpoint)

    # Parse the URL components.
    parsed = urllib.parse.urlparse(raw_url)

    # Validate domain against allowed list.
    netloc_parts = parsed.netloc.split(":")
    domain = netloc_parts[0].lower()
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Domain '{domain}' is not allowed for OAuth callbacks. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    # Add the state query parameter safely.
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    query["state"] = [verification_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the full URL.
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