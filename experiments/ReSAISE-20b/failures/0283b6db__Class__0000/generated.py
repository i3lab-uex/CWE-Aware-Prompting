#!/usr/bin/env python3
"""
Utility to generate a Single Sign-On (SSO) redirect URL.

The function validates the return URL against a list of allowed domains to
prevent CWE-610: Externally Controlled Reference to a Resource in Another Sphere.
"""

from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

# Example set of allowed domains. In production this should be populated
# from a secure configuration source.
ALLOWED_RETURN_DOMAINS = {
    "example.com",
    "app.example.org",
    "trusted-site.net",
}


def _is_allowed_return_url(return_url: str) -> bool:
    """
    Check if the return URL's domain is in ALLOWED_RETURN_DOMAINS.
    The comparison is case‑insensitive and ignores subdomains if not
    explicitly listed.

    :param return_url: The URL to validate.
    :return: True if allowed, False otherwise.
    """
    try:
        parsed = urlparse(return_url)
    except Exception:
        return False

    # Extract the hostname; if missing, consider it invalid
    host = parsed.hostname or ""
    host = host.lower()

    # Direct match check
    if host in ALLOWED_RETURN_DOMAINS:
        return True

    # Check if the domain ends with an allowed domain (e.g., sub.example.com)
    for allowed in ALLOWED_RETURN_DOMAINS:
        if host == allowed or host.endswith("." + allowed):
            return True

    return False


def generate_sso_redirect(
    sso_endpoint: str,
    user_id: str,
    return_url: str,
) -> str:
    """
    Generate a secure SSO redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base URL of the SSO service.
    user_id : str
        Unique identifier for the user.
    return_url : str
        URL to redirect back after authentication.

    Returns
    -------
    str
        A fully formed SSO redirect URL with encoded parameters.

    Raises
    ------
    ValueError
        If the return_url is not from an allowed domain.
    """
    if not _is_allowed_return_url(return_url):
        raise ValueError(f"Return URL domain is not allowed: {return_url}")

    # Parse the base endpoint to preserve any existing query parameters
    parsed_endpoint = urlparse(sso_endpoint)
    existing_params = parse_qs(parsed_endpoint.query)

    # Prepare new parameters
    params = {
        **{k: v[0] for k, v in existing_params.items()},  # flatten existing params
        "user_id": user_id,
        "return_url": return_url,
    }

    # Build the new query string
    new_query = urlencode(params, doseq=False)

    # Construct the final URL
    redirect_url = urlunparse(
        (
            parsed_endpoint.scheme,
            parsed_endpoint.netloc,
            parsed_endpoint.path,
            parsed_endpoint.params,
            new_query,
            parsed_endpoint.fragment,
        )
    )

    return redirect_url