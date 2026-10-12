import re
from urllib.parse import urlparse, urlunparse

# A small helper to extract the registered domain (e.g. example.com)
def _registered_domain(netloc: str) -> str:
    """
    Return the registered domain from a netloc.
    Handles IPv4/IPv6 addresses and ignores ports.
    """
    # Remove port if present
    host = netloc.split(":")[0]
    # For IPv6 addresses, strip brackets
    host = re.sub(r"^\[([0-9a-fA-F:]+)\]$", r"\1", host)

    # Split into labels
    parts = host.split(".")
    if len(parts) < 2:
        # IP addresses or single label domains
        return host.lower()

    # Return the last two labels (e.g. example.com)
    return ".".join(parts[-2:]).lower()


# List of approved domains (registered domain only)
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "myapp.io",
}

# Allowed schemes
ALLOWED_SCHEMES = {"http", "https"}


def process_url_redirect(input_url: str) -> str:
    """
    Validate and return a safe URL for redirection.

    Parameters
    ----------
    input_url : str
        The user supplied URL to redirect to.

    Returns
    -------
    str
        A fully qualified, safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the domain is not approved, or if the URL is malformed.
    """
    if not isinstance(input_url, str) or not input_url.strip():
        raise ValueError("input_url must be a non-empty string")

    parsed = urlparse(input_url)

    # Ensure we have a scheme
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https)")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme '{parsed.scheme}' is not allowed")

    # Ensure netloc (domain) exists
    if not parsed.netloc:
        raise ValueError("URL must include a host component")

    # Extract the registered domain and check against whitelist
    reg_domain = _registered_domain(parsed.netloc)
    if reg_domain not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{reg_domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it is canonical
    safe_url = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return safe_url