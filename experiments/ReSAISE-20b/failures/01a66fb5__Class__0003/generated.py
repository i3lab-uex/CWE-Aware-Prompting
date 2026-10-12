import urllib.parse

# Example allowed CDN domains; replace with actual safe domains.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.s3.amazonaws.com"
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a fully qualified CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        The base URL of the CDN (e.g., 'https://cdn.example.com/')
    resource_identifier : str
        Identifier of the resource (e.g., 'image123.png')
    type_of_resource : str
        Type of the resource (e.g., 'image', 'script')

    Returns
    -------
    str
        The fully constructed CDN URL.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Sanitize inputs: strip leading/trailing whitespace
    cdn_url_base = cdn_url_base.strip()
    resource_identifier = resource_identifier.strip().lstrip("/")
    type_of_resource = type_of_resource.strip().rstrip("/")

    # Ensure the base URL has a scheme; default to https if missing
    parsed_base = urllib.parse.urlparse(cdn_url_base)
    if not parsed_base.scheme:
        cdn_url_base = f"https://{cdn_url_base}"
        parsed_base = urllib.parse.urlparse(cdn_url_base)

    # Build the path component
    path_parts = [type_of_resource, resource_identifier]
    safe_path = "/".join(part.strip("/") for part in path_parts if part)
    # Construct the full URL using urljoin to handle trailing slashes correctly
    candidate_url = urllib.parse.urljoin(cdn_url_base.rstrip("/") + "/", safe_path)

    # Validate the resulting domain
    parsed_candidate = urllib.parse.urlparse(candidate_url)
    netloc_lower = parsed_candidate.netloc.lower()

    if netloc_lower not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {netloc_lower}")

    return candidate_url