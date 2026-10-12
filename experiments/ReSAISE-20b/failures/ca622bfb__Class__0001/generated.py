#!/usr/bin/env python3
"""
Utility for constructing a secure OAuth callback URL.

The function validates that the resulting callback URL points to an
authorized domain, protecting against CWE‑610 (Externally Controlled Reference).
"""

import urllib.parse
from typing import Set

# Define the set of domains that are allowed to receive OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add additional trusted domains here.
}


def assemble_oauth_callback_url(
    root_url: str, path_for_callback: str, session_token: str
) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    root_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_for_callback : str
        The relative path that will handle the OAuth callback
        (e.g., "/auth/callback").
    session_token : str
        A state token used to verify the OAuth transaction.

    Returns
    -------
    str
        The complete callback URL, including query parameters.

    Raises
    ------
    ValueError
        If the resolved callback URL resolves to a domain that is not in
        ALLOWED_CALLBACK_DOMAINS.
    """
    if not root_url or not path_for_callback:
        raise ValueError("root_url and path_for_callback must be non-empty strings")

    # Ensure root_url has a scheme; default to https if missing.
    parsed_root = urllib.parse.urlparse(root_url)
    if not parsed_root.scheme:
        root_url = f"https://{root_url}"
        parsed_root = urllib.parse.urlparse(root_url)

    # Join the base URL with the callback path.
    joined = urllib.parse.urljoin(root_url, path_for_callback)

    # Append the state parameter as a query string.
    callback_with_state = urllib.parse.urlunparse(
        (
            parsed_root.scheme,
            parsed_root.netloc,
            urllib.parse.urljoin(parsed_root.path, path_for_callback),
            "",  # params
            f"state={urllib.parse.quote_plus(session_token)}",
            "",
        )
    )

    # Validate the domain.
    callback_netloc = urllib.parse.urlparse(callback_with_state).netloc
    # Extract the hostname (ignore port).
    host = callback_netloc.split(":")[0].lower()

    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain '{host}' is not in the list of allowed domains."
        )

    return callback_with_state