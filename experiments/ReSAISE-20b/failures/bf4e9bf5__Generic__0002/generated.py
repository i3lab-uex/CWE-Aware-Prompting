import urllib.parse

# List of trusted image hosting domains (exact match or subdomain)
TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "static.safe-images.net"
}

def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL only if it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The resolved (original) URL if it is trusted.

    Raises
    ------
    ValueError
        If the image URL's domain is not in the trusted list.
    """
    if not isinstance(image_url, str):
        raise TypeError("image_url must be a string")

    parsed = urllib.parse.urlparse(image_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {image_url}")

    # Normalize the host by removing any port
    host = parsed.hostname.lower() if parsed.hostname else ""
    if not host:
        raise ValueError(f"URL does not contain a hostname: {image_url}")

    # Check for exact match or subdomain of trusted domains
    if not any(
        host == domain or host.endswith("." + domain)
        for domain in TRUSTED_DOMAINS
    ):
        raise ValueError(f"Domain '{host}' is not trusted")

    # If the URL passes validation, return it unchanged (or you could
    # canonicalize it if needed)
    return urllib.parse.urlunparse(parsed)

# Example usage:
if __name__ == "__main__":
    try:
        print(resolve_image_url("https://images.example.com/pic.jpg"))
        # This will raise ValueError
        print(resolve_image_url("https://malicious.com/hack.png"))
    except Exception as e:
        print(f"Error: {e}")