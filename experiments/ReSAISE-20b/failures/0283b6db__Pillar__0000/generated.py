#!/usr/bin/env python3
"""
Generate a secure SSO redirect URL.

The function validates the return URL against an allowed domain set,
escapes all parameters, and constructs a fully-qualified redirect
URL to the third‑party SSO service.
"""

import urllib.parse

# Set of domains that are allowed for the return URL
ALLOWED_RETURN_DOMAINS = {"example.com", "sub.example.org"}

def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Build a Single Sign-On redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service (e.g., "https://sso.example.com/auth").
    user_id : str
        The unique identifier of the user.
    return_url : str
        The URL to redirect back to after successful SSO.

    Returns
    -------
    str
        A fully‑qualified URL that the client should redirect to.

    Raises
    ------
    ValueError
        If `return_url` is not from an allowed domain.
    """
    # Parse the return URL to extract its domain
    parsed_return = urllib.parse.urlparse(return_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("Return URL must be a valid absolute URL")

    # Ensure the domain is in the allowed list
    # Normalize to lowercase and strip port numbers if present
    netloc = parsed_return.netloc.lower()
    # Remove port if any (e.g., example.com:8080 -> example.com)
    domain = netloc.split(":")[0]
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,  # Keep the original URL; it will be encoded
    }
    query_string = urllib.parse.urlencode(params, doseq=True)

    # Construct the final redirect URL
    # Use urljoin to safely combine base endpoint with query string
    # Ensure the endpoint ends with a slash if it doesn't already contain path components
    base = sso_endpoint.rstrip("/")
    final_url = f"{base}?{query_string}"

    return final_url

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(generate_sso_redirect(
#         "https://sso.example.com/auth",
#         "user123",
#         "https://example.com/dashboard"
#     ))