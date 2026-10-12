import re
from urllib.parse import urlparse

# List of fully-qualified domain names that are considered trusted.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.provider.net",
}

# Regular expression to detect private IP addresses.
PRIVATE_IP_RE = re.compile(
    r"""
    ^
    (
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return bool(PRIVATE_IP_RE.match(ip))


def _is_trusted_hostname(hostname: str) -> bool:
    """Check if the hostname is in the whitelist or resolves to a public IP."""
    # Exact match against known trusted domains.
    if hostname.lower() in TRUSTED_DOMAINS:
        return True

    # If the host is an IP address, ensure it is not private.
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", hostname):
        return not _is_private_ip(hostname)

    # For non-IP hosts, we consider them untrusted unless they are in the whitelist.
    return False


def inspect_api_url(url_to_inspect: str) -> str:
    """
    Validate that the supplied URL points to an external, trusted API endpoint.

    Parameters
    ----------
    url_to_inspect : str
        The URL to validate.

    Returns
    -------
    str
        The original URL if it is deemed safe.

    Raises
    ------
    ValueError
        If the URL does not use a supported scheme, points to an untrusted host,
        or attempts to reach a private/internal network.
    """
    if not isinstance(url_to_inspect, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(url_to_inspect)

    # Scheme must be HTTP or HTTPS.
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP/HTTPS allowed.")

    # Netloc (hostname + optional port) must be present.
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    # Separate hostname and port.
    hostname, _, port = parsed.netloc.partition(":")
    if not _is_trusted_hostname(hostname):
        raise ValueError(f"Hostname '{hostname}' is not in the list of trusted domains")

    # Optional: enforce that port is standard for HTTPS or HTTP if specified.
    if port:
        try:
            port_num = int(port)
        except ValueError:
            raise ValueError(f"Invalid port '{port}' in URL")
        if (parsed.scheme.lower() == "http" and port_num not in {80, 8080}) or \
           (parsed.scheme.lower() == "https" and port_num not in {443, 8443}):
            raise ValueError(f"Unusual port '{port_num}' for scheme '{parsed.scheme}'")

    # Ensure the URL does not target a private IP via hostname resolution.
    # (Optional) If DNS lookup is desired, uncomment the following lines:
    #
    # import socket
    # try:
    #     resolved_ip = socket.gethostbyname(hostname)
    # except socket.gaierror:
    #     raise ValueError(f"Hostname '{hostname}' could not be resolved")
    # if _is_private_ip(resolved_ip):
    #     raise ValueError(f"Hostname '{hostname}' resolves to private IP '{resolved_ip}'")

    return url_to_inspect