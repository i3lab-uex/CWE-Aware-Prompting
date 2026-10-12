import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (exact or suffix match)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedhost.org",
    "static.safe-site.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the given domain is trusted.
    Subdomains of a trusted domain are also considered trusted.
    """
    # Normalize to lowercase for comparison
    domain = domain.lower()
    return any(
        domain == td or domain.endswith("." + td)
        for td in _TRUSTED_DOMAINS
    )

def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the supplied image URL uses a trusted domain and
    an allowed scheme. Return the fully resolved URL if valid,
    otherwise raise ValueError.

    Parameters
    ----------
    pic_url : str
        The image URL to validate.

    Returns
    -------
    str
        The validated, fully resolved URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    # Parse the URL
    parsed = urlparse(pic_url)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Validate the domain
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Reconstruct the URL to ensure it is fully normalized
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower()
    )
    return urlunparse(cleaned)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        print(validate_picture_url("https://images.example.com/path/to/image.png"))
        # This will raise ValueError
        print(validate_picture_url("https://malicious.com/image.png"))
    except ValueError as e:
        print(f"Validation error: {e}")