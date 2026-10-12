import urllib.parse

# Predefined set of allowed CDN domains
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.content.net",
}

def build_cdn_resource_url(cdn_url: str, resource_identifier: str, resource_kind: str) -> str:
    """
    Build a fully qualified CDN URL for a given resource.

    Parameters
    ----------
    cdn_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        The unique identifier of the requested resource (e.g., "logo.png").
    resource_kind : str
        The type of the resource ("image", "script", etc.).

    Returns
    -------
    str
        The complete URL pointing to the requested resource on the CDN.

    Raises
    ------
    ValueError
        If the constructed URL does not resolve to a domain listed in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Sanitize inputs: strip leading/trailing whitespace
    cdn_url = cdn_url.strip()
    resource_identifier = resource_identifier.lstrip("/").strip()
    resource_kind = resource_kind.strip().lower()

    # Basic validation of inputs
    if not cdn_url or not resource_identifier or not resource_kind:
        raise ValueError("All arguments must be non-empty strings")

    # Ensure the CDN URL ends with a slash for proper joining
    if not cdn_url.endswith("/"):
        cdn_url += "/"

    # Construct the relative path for the resource
    relative_path = urllib.parse.urljoin(f"{resource_kind}/", resource_identifier)

    # Build the full URL
    full_url = urllib.parse.urljoin(cdn_url, relative_path)

    # Parse the resulting URL to validate its domain
    parsed = urllib.parse.urlparse(full_url)

    # The netloc might include port; strip it for domain comparison
    hostname = parsed.hostname or ""
    if hostname.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL '{full_url}' uses disallowed domain '{hostname}'. "
            "Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Ensure the scheme is HTTPS for security
    if parsed.scheme.lower() != "https":
        raise ValueError(
            f"Constructed URL '{full_url}' uses insecure scheme '{parsed.scheme}'. "
            "HTTPS is required."
        )

    return full_url