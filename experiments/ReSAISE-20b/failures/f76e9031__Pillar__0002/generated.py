import re
from urllib.parse import urlparse, urlunparse

# Approved domains (add more as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "secure.example.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}


def _is_approved_domain(host: str) -> bool:
    """
    Check whether the given host is in the list of approved domains.
    Sub‑domains are allowed only if they end with an approved domain
    and the entire host ends exactly at that boundary.
    """
    # Normalize to lowercase for comparison
    host = host.lower()
    for domain in APPROVED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it if safe for redirection.

    Parameters
    ----------
    target_url : str
        The URL input provided by the user.

    Returns
    -------
    str
        The validated, normalized URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the approved list,
        if the scheme is disallowed, or if the URL appears to be
        malformed or unsafe.
    """
    # Basic sanity check: must be a string
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(target_url)

    # Reject relative URLs or missing scheme
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute with a scheme and host")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Validate host
    if not _is_approved_domain(parsed.hostname or ""):
        raise ValueError(f"Domain '{parsed.hostname}' is not approved")

    # Reconstruct the URL to ensure it has no fragments or query parameters
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        ""   # fragment
    ))

    return safe_url


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        print(redirect_user_safely("https://sub.example.com/welcome"))
        # This will raise ValueError
        print(redirect_user_safely("http://malicious.com/evil"))
    except ValueError as e:
        print(f"Redirect blocked: {e}")