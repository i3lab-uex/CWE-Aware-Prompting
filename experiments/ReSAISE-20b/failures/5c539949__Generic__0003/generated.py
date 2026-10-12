import re
from urllib.parse import urlparse, urlunparse

# Define a set of approved domains.  Only URLs whose hostname matches one
# of these (or a sub‑domain of one, if desired) will be allowed.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Optional: allow sub‑domains of approved domains.
ALLOW_SUBDOMAINS = True

def _is_approved(hostname: str) -> bool:
    """
    Check if the given hostname is within the approved domain list.
    If sub‑domains are allowed, a match on any suffix of an approved
    domain is considered valid.
    """
    hostname = hostname.lower()
    if hostname in APPROVED_DOMAINS:
        return True

    if ALLOW_SUBDOMAINS:
        for domain in APPROVED_DOMAINS:
            # Ensure we match only whole subdomain parts, not just any suffix.
            if hostname.endswith("." + domain):
                return True
    return False

def secure_redirect_handler(redirect_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is
    approved. Raises ValueError otherwise.

    Parameters:
        redirect_url (str): The URL provided by the user.

    Returns:
        str: The validated, safe URL.

    Raises:
        ValueError: If the URL's domain is not approved or if parsing fails.
    """
    if not redirect_url:
        raise ValueError("Redirect URL must not be empty")

    # Parse the URL.  urllib.parse handles many edge cases, but we still
    # guard against malformed input.
    try:
        parsed = urlparse(redirect_url)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid URL format: {redirect_url}") from exc

    # Ensure the scheme is HTTP or HTTPS; otherwise it could be a
    # protocol-relative URL that might redirect to an unexpected domain.
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # Normalize the hostname by stripping port numbers and converting to
    # lower case.  urlparse already gives us a hostname without the port,
    # but we double‑check for safety.
    if not _is_approved(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Reconstruct the URL to ensure it has no fragment or query that might
    # alter its behavior in a malicious way.  If you wish to preserve those,
    # adjust the tuple accordingly.
    safe_parts = (
        parsed.scheme,
        parsed.netloc,  # includes port if present
        parsed.path,
        parsed.params,
        parsed.query,
        "",  # discard fragment for safety
    )
    return urlunparse(safe_parts)

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/page",
        "http://sub.trusted.org/resource?x=1#frag",
        "https://malicious.com/hack",
        "ftp://example.com/file",  # unsupported scheme
    ]

    for url in test_urls:
        try:
            print(f"Redirecting to: {secure_redirect_handler(url)}")
        except ValueError as e:
            print(f"Rejected '{url}': {e}")