import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered trusted image hosts.
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.securehost.net",
}

# Regular expression to validate domain names (RFC 1035).
_DOMAIN_RE = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)

def _is_trusted_domain(domain: str) -> bool:
    """
    Check if a domain is trusted. Subdomains of trusted domains are allowed.
    """
    # Normalise to lower case
    domain = domain.lower()
    if domain in _TRUSTED_DOMAINS:
        return True
    # Allow subdomains of trusted domains
    for tld in _TRUSTED_DOMAINS:
        if domain.endswith("." + tld):
            return True
    return False

def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL ensuring it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL of the image to validate and resolve.

    Returns
    -------
    str
        The resolved (canonical) URL if it belongs to a trusted domain.

    Raises
    ------
    ValueError
        If the URL is not a valid HTTP/HTTPS URL or its domain is not trusted.
    """
    if not isinstance(image_url, str):
        raise ValueError("image_url must be a string")

    parsed = urlparse(image_url)

    # Basic scheme validation
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL scheme must be http or https")

    # Validate netloc (domain)
    domain = parsed.netloc.split(":")[0]  # strip port if present
    if not _DOMAIN_RE.match(domain):
        raise ValueError(f"Invalid domain name: {domain}")

    if not _is_trusted_domain(domain):
        raise ValueError(f"Domain '{domain}' is not trusted")

    # Reconstruct the URL to normalise it (e.g., remove default ports)
    canonical = urlunparse(
        (
            parsed.scheme,
            domain,
            parsed.path or "",
            "",  # params
            parsed.query or "",
            ""   # fragment
        )
    )

    return canonical

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     test_url = "https://images.example.com/path/to/image.jpg?size=large"
#     print(resolve_image_url(test_url))