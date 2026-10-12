#!/usr/bin/env python3
"""
Utility for assembling a secure OAuth callback URL.
"""

from urllib.parse import urlparse, urljoin, urlencode, ParseResult
import re

# Example set of domains allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.myapp.org",
}

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain by removing leading `www.` and converting to lowercase.
    """
    return re.sub(r"^www\.", "", domain.lower())

def _extract_domain(url: str) -> str:
    """
    Extract the network location (domain + port if any) from a URL.
    """
    parsed = urlparse(url)
    return _normalize_domain(parsed.hostname or "")

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g., "https://myapp.com").
    callback_route : str
        The relative route for the OAuth callback handler (e.g., "/oauth/callback").
    token_state : str
        A unique state string to prevent CSRF attacks.

    Returns
    -------
    str
        The complete callback URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resolved callback domain is not in ``ALLOWED_CALLBACK_DOMAINS``
        and does not match the application domain.
    """
    # Ensure the base URL is absolute
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", application_url):
        raise ValueError("application_url must be an absolute URL with scheme")

    # Resolve the callback route against the application base
    full_url = urljoin(application_url.rstrip("/") + "/", callback_route.lstrip("/"))

    # Extract domains for comparison
    app_domain = _extract_domain(application_url)
    callback_domain = _extract_domain(full_url)

    # Security check: domain must be either the same as application
    # or listed in ALLOWED_CALLBACK_DOMAINS.
    if callback_domain != app_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state query parameter
    parsed = urlparse(full_url)
    query_params = dict([pair.split("=", 1) for pair in parsed.query.split("&") if "=" in pair]) \
        if parsed.query else {}
    query_params["state"] = token_state
    new_query = urlencode(query_params)

    # Reconstruct the URL with the updated query string
    final_url = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path,
        params=parsed.params,
        query=new_query,
        fragment=parsed.fragment
    ).geturl()

    return final_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     url = assemble_oauth_callback(
#         "https://myapp.com",
#         "/oauth/callback",
#         "unique_state_token_123"
#     )
#     print(url)