import urllib.parse
from typing import Set

# Example set of allowed callback domains. In a real application this should be
# configured externally (e.g., via environment variables or a config file).
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str
) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g., "https://app.example.com").
    callback_route : str
        The path to the OAuth callback handler (e.g., "/auth/callback").
    token_state : str
        A unique state value used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled callback URL, including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS
        and does not match the application domain.
    """
    # Normalise the base URL and the callback route
    parsed_app = urllib.parse.urlparse(application_url.rstrip("/"))
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError("application_url must be a valid absolute URL")

    # Join the base with the callback route
    joined = urllib.parse.urljoin(application_url, callback_route.lstrip("/"))
    parsed_cb = urllib.parse.urlparse(joined)

    # Validate domain
    callback_domain = parsed_cb.hostname
    if not callback_domain:
        raise ValueError("Callback URL must have a valid hostname")

    # Check if the callback domain is either allowed or matches the application domain
    app_domain = parsed_app.hostname
    if callback_domain not in ALLOWED_CALLBACK_DOMAINS and callback_domain != app_domain:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not permitted. "
            "Allowed domains: {}.".format(", ".join(sorted(ALLOWED_CALLBACK_DOMAINS)))
        )

    # Build query string with state parameter
    query = urllib.parse.parse_qs(parsed_cb.query)
    query["state"] = [token_state]
    encoded_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL with the new query string
    assembled = urllib.parse.urlunparse(
        (
            parsed_cb.scheme,
            parsed_cb.netloc,
            parsed_cb.path,
            parsed_cb.params,
            encoded_query,
            parsed_cb.fragment,
        )
    )

    return assembled