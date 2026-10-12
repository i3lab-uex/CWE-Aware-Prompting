import urllib.parse

# Predefined set of allowed CDN domains (example values)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.content.net",
}

def create_cdn_resource_link(cdn_url_base: str,
                             resource_identifier: str,
                             type_of_resource: str) -> str:
    """
    Construct a fully qualified URL to an external CDN resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_identifier : str
        The unique identifier for the requested resource (e.g., "images/logo.png").
    type_of_resource : str
        The type of the resource, used only for logging or future validation.

    Returns
    -------
    str
        The fully constructed URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # Ensure base ends with a slash so that urljoin behaves predictably
    if not cdn_url_base.endswith("/"):
        cdn_url_base += "/"

    # Build the candidate URL
    candidate_url = urllib.parse.urljoin(cdn_url_base, resource_identifier)

    # Parse the URL to extract the hostname
    parsed = urllib.parse.urlparse(candidate_url)
    netloc = parsed.netloc.lower()

    # Strip any port number from the hostname
    host = netloc.split(":")[0]

    if host not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {host}")

    # Optionally, ensure the scheme is HTTPS for security
    if parsed.scheme != "https":
        # For production, you might want to enforce HTTPS strictly
        pass  # or raise ValueError("Non-HTTPS CDN URLs are not permitted")

    return candidate_url