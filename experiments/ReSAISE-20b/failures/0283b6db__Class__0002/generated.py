#!/usr/bin/env python3
"""
SSO redirect URL generator with domain validation.

Author: OpenAI ChatGPT
"""

import urllib.parse

# Domains that are allowed to be used as a return URL after SSO.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add more trusted domains here
}


def _is_allowed_domain(hostname: str) -> bool:
    """
    Check whether the given hostname ends with one of the allowed domains.
    Subdomains are considered valid if they end exactly with an allowed domain.
    """
    hostname = hostname.lower()
    for domain in ALLOWED_RETURN_DOMAINS:
        # Ensure we match the full domain part, not just a prefix
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False


def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service (e.g., "https://sso.example.com/login").
    user_id : str
        The unique identifier of the user.
    return_url : str
        Absolute URL to redirect to after successful SSO.

    Returns
    -------
    str
        The fully constructed SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If `return_url` is not from an allowed domain or if it is not a valid absolute URL.
    """
    # Validate the return_url
    parsed_return = urllib.parse.urlparse(return_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("return_url must be an absolute URL")

    if not _is_allowed_domain(parsed_return.hostname or ""):
        raise ValueError(f"return_url domain '{parsed_return.hostname}' is not allowed")

    # Parse the SSO endpoint to manipulate its query parameters
    parsed_sso = urllib.parse.urlparse(sso_endpoint)

    # Prepare new query parameters (existing ones are preserved)
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)

    # Add or overwrite the user_id and return_url parameters
    existing_params["user_id"] = [user_id]
    existing_params["return_url"] = [return_url]

    # Build the final query string
    new_query = urllib.parse.urlencode(existing_params, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            new_query,
            parsed_sso.fragment,
        )
    )

    return final_url