#!/usr/bin/env python3
"""
OAuth callback URL generator with domain validation.
"""

import urllib.parse

# Example set of allowed domains for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
    # Add additional allowed domains as needed.
}


def create_oauth_callback_url(base_url: str, callback_path: str, state: str) -> str:
    """
    Construct a fully qualified OAuth callback URL and ensure it uses an allowed domain.

    Parameters
    ----------
    base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    callback_path : str
        The path for the OAuth callback (e.g., "/auth/callback").
    state : str
        A unique, unguessable state string to protect against CSRF.

    Returns
    -------
    str
        The complete OAuth callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL does not belong to an allowed domain.
    """
    # Normalize and join base_url with the callback path
    full_path = urllib.parse.urljoin(base_url.rstrip("/") + "/", callback_path.lstrip("/"))

    # Parse the URL to manipulate query parameters safely
    parsed = urllib.parse.urlparse(full_path)

    # Encode the state parameter to prevent injection attacks
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["state"] = [state]
    new_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the full URL with the new query string
    validated_url = urllib.parse.urlunparse(
        parsed._replace(query=new_query)
    )

    # Extract the hostname (without port) and normalize to lowercase
    host = parsed.hostname.lower() if parsed.hostname else ""
    # Validate against the allowed domains set
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Callback URL domain '{host}' is not allowed.")

    return validated_url


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = create_oauth_callback_url(
#         "https://app.example.com",
#         "/oauth/callback",
#         "a-unique-state-string"
#     )
#     print(url)