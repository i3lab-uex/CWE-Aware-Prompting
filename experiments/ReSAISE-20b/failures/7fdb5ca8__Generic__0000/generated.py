import re
import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# List of domains considered trusted for external API calls.
TRUSTED_DOMAINS = {
    # Example domains – replace or extend as needed
    "api.example.com",
    "services.trustedpartner.org",
    "data.provider.net",
}

# Regular expression to detect IP addresses in the hostname
IP_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")


def _is_private_ip(ip: str) -> bool:
    """Return True if the given IP is in a private or reserved range."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address
        return False


def _resolve_hostname(hostname: str) -> list[str]:
    """Return a list of IP addresses that the hostname resolves to."""
    try:
        # gethostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        _, _, addr_list = socket.gethostbyname_ex(hostname)
        return addr_list
    except socket.gaierror:
        # Hostname could not be resolved
        return []


def verify_api_address(url_to_check: str) -> str:
    """
    Verify that the provided URL points to a trusted external API endpoint.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        A normalized, validated URL that can be safely used for external API calls.

    Raises
    ------
    ValueError
        If the URL is malformed, resolves to an internal IP address,
        or its hostname is not in the list of trusted domains.
    """
    # Basic URL parsing
    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include a scheme and host")

    # Ensure HTTPS or HTTP only (no file://, ftp:// etc.)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Check if the hostname is an IP address
    if IP_RE.match(hostname):
        # Direct IP – reject unless it is a trusted IP (rare case)
        if _is_private_ip(hostname):
            raise ValueError("Direct IP addresses are not allowed")
        # Optionally add a list of trusted IPs if needed
    else:
        # Resolve the hostname to its IP addresses
        ip_list = _resolve_hostname(hostname)
        if not ip_list:
            raise ValueError(f"Hostname '{hostname}' could not be resolved")

        # Reject if any resolved IP is private or reserved
        for ip in ip_list:
            if _is_private_ip(ip):
                raise ValueError(
                    f"Hostname '{hostname}' resolves to private IP {ip}"
                )

        # Verify that the hostname ends with a trusted domain
        if not any(hostname == td or hostname.endswith("." + td) for td in TRUSTED_DOMAINS):
            raise ValueError(
                f"Hostname '{hostname}' is not in the list of trusted domains"
            )

    # Reconstruct a normalized URL (remove default ports, etc.)
    netloc = parsed.netloc
    if ":" in netloc:
        host_part, port_str = netloc.split(":", 1)
        try:
            port = int(port_str)
            if (parsed.scheme == "http" and port == 80) or (
                parsed.scheme == "https" and port == 443
            ):
                netloc = host_part  # drop default port
        except ValueError:
            pass

    normalized = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return normalized