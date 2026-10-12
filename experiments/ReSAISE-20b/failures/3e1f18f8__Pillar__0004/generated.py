#!/usr/bin/env python3
"""
SSO redirect URL constructor with domain validation.
"""

from urllib.parse import (
    urlparse,
    parse_qs,
    urlencode,
    ParseResult,
)

# Set of domains that are allowed to be used as a return URL.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "sub.example.org",
    # Add other allowed domains here.
}


def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str,
) -> str:
    """
    Build a fully‑qualified SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base endpoint of the SSO provider (e.g. 'https://sso.example.com/auth').
    user_identifier : str
        Unique identifier of the user (e.g. a UUID or username).
    redirect_uri : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The complete redirect URL ready to send the user to the SSO provider.

    Raises
    ------
    ValueError
        If `redirect_uri` is malformed or its domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # ---- 1. Validate the redirect URI ------------------------------------
    parsed_redirect = urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect URI: '{redirect_uri}'")

    # Extract hostname (domain) and compare against allowed list.
    host = parsed_redirect.hostname
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{host}' is not permitted. Allowed domains: "
            f"{', '.join(sorted(ALLOWED_RETURN_DOMAINS))}"
        )

    # ---- 2. Prepare query parameters --------------------------------------
    # Parse any existing query string on the auth endpoint.
    base_endpoint = urlparse(auth_service_endpoint)
    existing_params = {
        k: v[0] for k, v in parse_qs(base_endpoint.query).items()
    }

    # Add/override with required SSO parameters.
    existing_params.update(
        {
            "user": user_identifier,
            "redirect_uri": redirect_uri,  # urlencode will handle encoding.
        }
    )

    # Reconstruct the full URL with updated query string.
    new_query = urlencode(existing_params, doseq=False)

    final_url = ParseResult(
        scheme=base_endpoint.scheme,
        netloc=base_endpoint.netloc,
        path=base_endpoint.path,
        params=base_endpoint.params,
        query=new_query,
        fragment=base_endpoint.fragment,
    ).geturl()

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = construct_sso_redirect(
            auth_service_endpoint="https://sso.example.com/auth",
            user_identifier="user123",
            redirect_uri="https://example.com/welcome?foo=bar",
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print("Error constructing SSO redirect:", exc)