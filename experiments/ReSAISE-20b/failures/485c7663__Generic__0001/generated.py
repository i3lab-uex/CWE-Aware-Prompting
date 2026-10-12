import socket
from urllib.parse import urlparse, urlunparse
import ipaddress

def enforce_api_security(api_endpoint: str) -> str:
    """
    Verify that the given API endpoint URL points to a secure, external resource.
    
    Parameters
    ----------
    api_endpoint : str
        The URL that needs to be verified.
    
    Returns
    -------
    str
        The original URL if it passes all checks.
    
    Raises
    ------
    ValueError
        If the URL is malformed, does not use HTTPS,
        or resolves to a private/loopback IP address.
    """
    
    # Parse the URL
    parsed = urlparse(api_endpoint)
    
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: '{api_endpoint}'. Must include scheme and host.")
    
    # Enforce HTTPS for external API calls
    if parsed.scheme.lower() != 'https':
        raise ValueError(f"Only HTTPS URLs are allowed for API endpoints. Got scheme '{parsed.scheme}'.")
    
    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"URL does not contain a valid hostname: '{api_endpoint}'.")
    
    # Resolve the host to IP addresses
    try:
        addr_info = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve hostname '{hostname}': {exc}") from exc
    
    # Check each IP address for internal/private ranges
    for entry in addr_info:
        ip_str = entry[4][0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue  # Skip invalid IPs
        
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            raise ValueError(
                f"Disallowed internal IP address '{ip_str}' for host '{hostname}'. "
                "Potential SSRF detected."
            )
    
    # Reconstruct the URL to ensure consistent formatting
    safe_url = urlunparse(parsed)
    return safe_url

# Example usage (for testing purposes only):
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/data",
        "http://localhost/api",
        "https://192.168.1.10/resource",
        "ftp://example.com/file"
    ]
    
    for url in test_urls:
        try:
            print(f"✅ {enforce_api_security(url)}")
        except ValueError as e:
            print(f"❌ {url} -> {e}")