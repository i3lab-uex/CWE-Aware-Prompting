import urllib.parse
from typing import Set

# Example allowed domains; in a real project this would be defined elsewhere.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}

def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str
) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The endpoint that handles the OAuth callback (e.g., "/oauth/callback").
    session_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled OAuth callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``
        and does not match the main URL's domain.
    """
    # Ensure we have a proper base URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError("Invalid main_url: must include scheme and domain")

    # Build the callback URL by joining the base with the endpoint
    joined = urllib.parse.urljoin(main_url, redirect_endpoint)

    # Parse the resulting URL to inspect its components
    parsed_callback = urllib.parse.urlparse(joined)

    # Verify that the callback URL is within an allowed domain
    callback_domain = parsed_callback.netloc.lower()
    main_domain = parsed_main.netloc.lower()

    if callback_domain not in ALLOWED_CALLBACK_DOMAINS and callback_domain != main_domain:
        raise ValueError(
            f"Disallowed OAuth callback domain: {callback_domain}. "
            "Must be either the main application domain or in ALLOWED_CALLBACK_DOMAINS."
        )

    # Append the state parameter securely
    query = urllib.parse.parse_qs(parsed_callback.query)
    query["state"] = [session_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_callback.scheme,
            parsed_callback.netloc,
            parsed_callback.path,
            parsed_callback.params,
            new_query,
            parsed_callback.fragment,
        )
    )

    return final_url