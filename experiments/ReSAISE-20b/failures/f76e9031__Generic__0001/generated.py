import re
from urllib.parse import urlparse, urlunparse

# Define the set of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-domain.net",
}

# Regular expression to ensure the URL uses http or https scheme.
SCHEME_REGEX = re.compile(r"^(https?)://", re.IGNORECASE)


def redirect_user_safely(target_url: str) -> str:
    """
    Validate and return a user‑supplied URL that is safe to redirect to.

    Parameters
    ----------
    target_url : str
        The URL provided by the user.

    Returns
    -------
    str
        A sanitized, validated URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not use http/https scheme or its domain is not in the approved list.
    """
    if not isinstance(target_url, str):
        raise ValueError("URL must be a string")

    # Strip surrounding whitespace
    target_url = target_url.strip()

    # Ensure the URL has a scheme and is http or https
    if not SCHEME_REGEX.match(target_url):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(target_url)

    # Reject URLs that have no network location (netloc)
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Normalise the domain to lowercase for comparison
    domain = parsed.hostname.lower() if parsed.hostname else ""

    # Check that the domain is exactly in the approved list or a subdomain of an approved domain
    if not any(
        domain == approved or domain.endswith("." + approved)
        for approved in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it has no fragments or query parameters that might be malicious
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        print(redirect_user_safely("https://example.com/path?param=1"))
    except ValueError as e:
        print(f"Invalid URL: {e}")