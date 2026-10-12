import urllib.parse
from typing import Iterable

# Define a set of domains that are considered safe for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "myapp.example.org",
    # Add additional trusted domains here.
}


def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str,
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's main base URL (e.g., "https://myapp.example.org").
    callback_endpoint : str
        The relative path for the OAuth callback endpoint (e.g., "/auth/callback").
    verification_state : str
        A unique value used to verify the integrity of the OAuth request flow.

    Returns
    -------
    str
        The fully qualified callback URL with an appended `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the base URL and endpoint to avoid double slashes.
    base = app_base_url.rstrip("/")
    endpoint = callback_endpoint.lstrip("/")

    # Build the raw URL.
    raw_url = f"{base}/{endpoint}"

    # Append the state query parameter safely.
    parsed = urllib.parse.urlparse(raw_url)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = verification_state
    new_query = urllib.parse.urlencode(query_params)

    # Reconstruct the full URL.
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Verify that the domain is allowed.
    netloc = urllib.parse.urlparse(final_url).netloc
    # Strip port if present.
    domain = netloc.split(":")[0].lower()

    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {domain}. Allowed domains are "
            f"{', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}."
        )

    return final_url