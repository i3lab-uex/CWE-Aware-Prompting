import re
from urllib.parse import urlparse, urljoin

# Whitelist of trusted image hosting domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedimg.org",
    "assets.safe-site.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Check if the hostname (netloc) is in the TRUSTED_DOMAINS set.
    Handles subdomains by checking the registered domain portion.
    """
    # Normalize to lower case
    host = netloc.lower()
    # Strip port if present
    host = host.split(":")[0]
    return host in TRUSTED_DOMAINS

def validate_image_source(img_src: str) -> str:
    """
    Validate that the supplied image URL is from a trusted domain and
    has an allowed scheme. Returns the fully resolved absolute URL.

    Parameters:
        img_src (str): The image URL to validate and resolve.

    Returns:
        str: The validated, fully-qualified URL.

    Raises:
        ValueError: If the URL is malformed, uses an unsupported scheme,
                    or points to an untrusted domain.
    """
    if not isinstance(img_src, str) or not img_src.strip():
        raise ValueError("img_src must be a non-empty string")

    # Resolve relative URLs against a base (empty means no change)
    resolved = urljoin("", img_src.strip())

    parsed = urlparse(resolved)

    # Scheme must be http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain must be trusted
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # Basic sanity check for image file extensions
    if not re.search(r"\.(png|jpe?g|gif|webp)(\?.*)?$", parsed.path, re.IGNORECASE):
        raise ValueError("URL does not point to a recognized image file")

    # Return the absolute URL (reconstruct in case urljoin modified it)
    return parsed.geturl()