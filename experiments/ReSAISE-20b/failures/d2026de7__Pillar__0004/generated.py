import re
from urllib.parse import urlparse, urlunparse

# List of approved RSS providers (domains or sub‑domain patterns)
TRUSTED_PROVIDERS = {
    r"^news\.nytimes\.com$",
    r"^rss\.theguardian\.com$",
    r"^feeds\.bbc\.co\.uk$",
    r"^rss\.reuters\.com$",
    r"^feeds\.cnn\.com$",
}

# Regex to detect private IP ranges (CWE‑664 relevant check)
PRIVATE_IP_REGEX = re.compile(
    r"^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|127\.)"
)

def _is_private_ip(netloc: str) -> bool:
    """
    Simple check to see if the hostname resolves to a private IP.
    For the purpose of this validation we only inspect numeric hosts.
    """
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", netloc):
        return bool(PRIVATE_IP_REGEX.match(netloc))
    return False

def _is_trusted_domain(domain: str) -> bool:
    """Return True if the domain matches any of the trusted provider patterns."""
    for pattern in TRUSTED_PROVIDERS:
        if re.match(pattern, domain):
            return True
    return False

def check_rss_address(rss_address: str) -> str:
    """
    Validate that an RSS feed URL belongs to a trusted provider and does not
    point to any internal or private network.

    Parameters:
        rss_address (str): The URL of the RSS feed to validate.

    Returns:
        str: A sanitized version of the original URL if it passes validation.

    Raises:
        ValueError: If the URL is not from an approved provider or attempts
                    to access a restricted internal network.
    """
    if not isinstance(rss_address, str):
        raise ValueError("RSS address must be a string")

    parsed = urlparse(rss_address)

    # Ensure scheme is HTTP or HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # Normalize netloc to lower case
    host = parsed.hostname or ""
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address which is not allowed")

    # Reject internal domain names (e.g., .local, .internal)
    if re.search(r"\.(local|internal)$", host):
        raise ValueError("URL points to an internal domain which is not allowed")

    # Validate against trusted providers
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not an approved RSS provider")

    # Reconstruct the URL to strip any fragments or query parameters
    sanitized = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

    return sanitized