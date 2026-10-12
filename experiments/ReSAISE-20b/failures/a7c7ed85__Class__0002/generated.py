#!/usr/bin/env python3
"""
Utility to validate image URLs against a whitelist of trusted domains.

The function `validate_image_url` parses the supplied URL, checks that
the scheme is either HTTP or HTTPS and that the host (or a sub‑domain of
it) belongs to one of the approved image hosting providers.  If all
checks pass, the original URL is returned unchanged; otherwise a
`ValueError` is raised.

This implementation avoids unintentionally acting as an HTTP proxy or
forwarding requests on behalf of the caller, thereby mitigating CWE‑441.
"""

from urllib.parse import urlparse
import sys

# Whitelist of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "media.giphy.com",
}

def _is_trusted_domain(host: str) -> bool:
    """
    Determine whether the supplied host (e.g. 'i.imgur.com') is a
    sub‑domain of any domain in TRUSTED_DOMAINS.
    """
    # Normalise host: strip port if present
    host = host.split(":")[0].lower()
    # Direct match or sub‑domain match
    return any(
        host == domain or host.endswith("." + domain)
        for domain in TRUSTED_DOMAINS
    )

def validate_image_url(img_url: str) -> str:
    """
    Validate an image URL against a whitelist of trusted domains.

    Parameters
    ----------
    img_url : str
        The image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and trusted.

    Raises
    ------
    ValueError
        If the URL scheme is not HTTP(S) or if the domain is not trusted.
    """
    parsed = urlparse(img_url)

    # Check scheme
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Check host
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (host)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc}")

    # All checks passed; return the original URL unchanged
    return img_url

# Example usage (remove or comment out when importing as a module)
if __name__ == "__main__":
    for url in sys.argv[1:]:
        try:
            print(f"Valid URL: {validate_image_url(url)}")
        except ValueError as e:
            print(f"Invalid URL: {url} -> {e}")