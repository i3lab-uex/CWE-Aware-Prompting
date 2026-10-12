import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.local",  # internal service
}

# Allowed schemes for redirection.
ALLOWED_SCHEMES = {"http", "https"}


def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain by stripping the port (if any) and lower‑casing.
    """
    if ":" in domain:
        domain, _ = domain.split(":", 1)
    return domain.lower()


def redirect_user_safely(target_url: str) -> str:
    """
    Validate a user‑supplied URL and return it only if its domain is in the
    approved list. Raises ValueError otherwise.

    Args:
        target_url: The URL supplied by the user.

    Returns:
        A validated absolute URL that can be safely used for redirection.

    Raises:
        ValueError: If the URL is not absolute, has an unapproved domain,
                    or uses a disallowed scheme.
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # Ensure we have an absolute URL with a scheme.
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain a scheme")

    # Only allow http/https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Normalise the domain (strip port, lowercase)
    domain = _normalize_domain(parsed.netloc)

    # Check against the approved domains
    if domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not approved for redirection")

    # Re‑assemble the URL to ensure no hidden components (e.g., userinfo)
    safe_url = urlunparse((
        parsed.scheme,
        domain,               # netloc without port
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""                    # strip fragment
    ))

    return safe_url


# Example usage (for demonstration only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    try:
        print(redirect_user_safely("https://example.com/path?query=1"))
    except ValueError as e:
        print(f"Redirect blocked: {e}")