import re
import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of trusted providers (domain names). Add or remove as needed.
_TRUSTED_PROVIDERS = {
    "feeds.reddit.com",
    "rss.nytimes.com",
    "blogspot.com",
    "medium.com",
    "news.ycombinator.com",
    "rss.cnn.com",
}

# Regular expression to validate the URL scheme.
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_ip_private(host: str) -> bool:
    """
    Resolve the host to IP addresses and check if any are private.
    """
    try:
        for addrinfo in socket.getaddrinfo(host, None):
            ip = addrinfo[4][0]
            if ipaddress.ip_address(ip).is_private:
                return True
    except socket.gaierror:
        # Host could not be resolved; treat as unsafe.
        return True
    return False


def _normalize_url(parsed: "ParseResult") -> str:
    """
    Reconstruct the URL ensuring no path traversal or query side‑effects.
    """
    # Strip fragment
    parsed = parsed._replace(fragment="")
    # Normalize path to avoid directory traversal
    path_parts = [p for p in parsed.path.split("/") if p and not re.match(r"^\.\.?$", p)]
    normalized_path = "/" + "/".join(path_parts)
    parsed = parsed._replace(path=normalized_path)
    return urlunparse(parsed)


def secure_feed_link(rss_url: str) -> str:
    """
    Validate an RSS feed URL against a whitelist of trusted providers and
    ensure it does not resolve to a private/internal network address.

    Parameters:
        rss_url (str): The URL to validate and sanitize.

    Returns:
        str: A sanitized, validated RSS feed URL.

    Raises:
        ValueError: If the URL is malformed, not HTTPS/HTTP,
                    points to an untrusted domain, or resolves to a private IP.
    """
    # Basic scheme validation
    if not _SCHEME_RE.match(rss_url):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(rss_url)

    # Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check domain against whitelist (case‑insensitive)
    host_lower = parsed.hostname.lower()
    if not any(host_lower == provider or host_lower.endswith("." + provider)
               for provider in _TRUSTED_PROVIDERS):
        raise ValueError(f"Domain '{parsed.hostname}' is not in the trusted provider list")

    # Resolve IP and ensure it is not private
    if _is_ip_private(parsed.hostname):
        raise ValueError(f"Hostname '{parsed.hostname}' resolves to a private IP address")

    # Normalize the URL (strip fragments, clean path)
    sanitized = _normalize_url(parsed)

    return sanitized