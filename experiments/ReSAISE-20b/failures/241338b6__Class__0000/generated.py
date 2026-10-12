import socket
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Configuration: a set of approved domains and allowed schemes
# --------------------------------------------------------------------------- #
APPROVED_DOMAINS = {
    "api.openai.com",
    "api.github.com",
    "api.example.com",  # add other approved domains here
}

APPROVED_SCHEMES = {"https"}   # we only allow HTTPS to avoid HTTP redirects


def _is_internal_ip(ip: str) -> bool:
    """
    Return True if the IP address is in a private or loopback range.
    Uses standard IPv4/IPv6 private ranges defined by RFC1918 and RFC4193.
    """
    try:
        addr = socket.inet_pton(socket.AF_INET, ip)
    except OSError:  # not IPv4
        try:
            addr = socket.inet_pton(socket.AF_INET6, ip)
        except OSError:  # not IPv4 or IPv6
            return True

    # Convert to integer for easy comparison
    if len(addr) == 4:  # IPv4
        octets = [int(b) for b in addr]
        if octets[0] == 10:
            return True
        if octets[0] == 172 and 16 <= octets[1] <= 31:
            return True
        if octets[0] == 192 and octets[1] == 168:
            return True
        if octets[0] == 127:   # loopback
            return True
    else:  # IPv6
        if addr.startswith(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff"):
            return True  # ::ffff:0:0/96
        if addr.startswith(b"\x00\x00"):
            return True  # ::/8 (implicit)
        if addr == b"\x00\x00\x00\x00\x00\x00\x00\x01":
            return True  # ::1

    return False


def _resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve the hostname to all IPv4/IPv6 addresses.
    Return a list of string IPs.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve hostname: {hostname}")

    return [info[4][0] for info in infos]


def verify_api_link(url_to_check: str) -> str:
    """
    Verify that the given URL points to an approved external API and is not
    targeting internal network addresses.

    Parameters:
        url_to_check (str): The URL to validate.

    Returns:
        str: The validated URL, unchanged if it passes all checks.

    Raises:
        ValueError: If the URL is malformed, not HTTPS, points to a disallowed
                    domain, or resolves to an internal IP address.
    """
    # Parse the URL and ensure it has a scheme, netloc
    parsed = urlparse(url_to_check)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host")

    # Enforce HTTPS
    if parsed.scheme.lower() not in APPROVED_SCHEMES:
        raise ValueError(f"Only {', '.join(APPROVED_SCHEMES)} scheme is allowed")

    # Normalize host to lower case for comparison
    hostname = parsed.hostname.lower()

    if hostname not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not approved")

    # Resolve the hostname to IP addresses
    ip_addresses = _resolve_hostname(hostname)

    # Ensure none of the resolved IPs are internal
    for ip in ip_addresses:
        if _is_internal_ip(ip):
            raise ValueError(f"Resolved IP {ip} is an internal address")

    # Reconstruct the URL to avoid any subtle variations (e.g., missing port)
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "/",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned