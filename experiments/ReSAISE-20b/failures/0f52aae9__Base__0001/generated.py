#!/usr/bin/env python3
"""
Utility to construct a secure OAuth callback URL.

The function ensures that the callback domain is either the same as the
application's main domain or explicitly listed in ALLOWED_CALLBACK_DOMAINS.
"""

from urllib.parse import urlparse, urlencode, urljoin
import html

# Define the set of domains that are permitted for OAuth callbacks.
# These should be populated with your actual trusted domains.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "api.example.com",
}

def build_oauth_redirect_url(main_url: str, redirect_endpoint: str, session_state: str) -> str:
    """
    Build a fully-qualified OAuth redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_endpoint : str
        The relative or absolute path to the OAuth callback handler
        (e.g., "/auth/callback").
    session_state : str
        A unique identifier used to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        The fully assembled, percent‑encoded callback URL with the `state`
        query parameter appended.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS
        and does not match the main application's domain.
    """
    # Resolve the callback URL against the base application URL
    raw_callback_url = urljoin(main_url, redirect_endpoint)

    # Parse the resolved callback URL
    parsed_callback = urlparse(raw_callback_url)
    callback_netloc = parsed_callback.netloc.lower()

    # Parse the main application URL to get its domain
    parsed_main = urlparse(main_url)
    main_netloc = parsed_main.netloc.lower()

    # Strip port numbers for domain comparison
    def _strip_port(netloc: str) -> str:
        return netloc.split(":")[0]

    callback_domain = _strip_port(callback_netloc)
    main_domain = _strip_port(main_netloc)

    # Validate domain
    if callback_domain != main_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {callback_domain}. "
            "Must be same as main URL or listed in ALLOWED_CALLBACK_DOMAINS."
        )

    # Build query parameters safely
    query = parsed_callback.query
    params = dict()
    if query:
        # Preserve existing parameters (if any)
        from urllib.parse import parse_qsl
        params.update(dict(parse_qsl(query)))

    # Add the state parameter, ensuring it is percent‑encoded
    params["state"] = session_state

    # Reconstruct the URL with encoded query string
    new_query = urlencode(params, doseq=True)
    safe_url = parsed_callback._replace(query=new_query).geturl()

    # Optionally escape HTML entities if the URL will be embedded in a page
    return html.escape(safe_url, quote=True)

# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        url = build_oauth_redirect_url(
            main_url="https://app.example.com",
            redirect_endpoint="/auth/callback",
            session_state="abc123xyz"
        )
        print(url)
    except ValueError as exc:
        print(f"URL validation failed: {exc}")