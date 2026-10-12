import urllib.parse

# Example set of safe CDN domains. Replace with the actual allowed domains.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.othercdn.org",
}

def create_cdn_resource_link(cdn_url_base: str, resource_identifier: str,
                              type_of_resource: str) -> str:
    """
    Construct a full CDN URL for the requested resource.

    Parameters
    ----------
    cdn_url_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com/").
    resource_identifier : str
        Identifier of the requested resource (e.g. "images/logo.png").
    type_of_resource : str
        Type of the resource (e.g. "image", "script").

    Returns
    -------
    str
        Fully qualified URL pointing to the requested external resource.

    Raises
    ------
    ValueError
        If the generated URL does not resolve to an allowed CDN domain.
    """
    # Sanitize inputs: strip leading/trailing whitespace and ensure strings
    cdn_url_base = str(cdn_url_base).strip()
    resource_identifier = str(resource_identifier).strip().lstrip("/")
    type_of_resource = str(type_of_resource).strip()

    # Construct the raw URL
    # Use urljoin to correctly handle trailing slashes
    raw_url = urllib.parse.urljoin(cdn_url_base, f"{type_of_resource}/{resource_identifier}")

    # Parse the URL to inspect components
    parsed = urllib.parse.urlparse(raw_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL constructed: {raw_url}")

    # Normalize the domain for comparison (lowercase, strip port)
    netloc = parsed.netloc.split(":")[0].lower()

    # Verify that the domain is in the allowed set or ends with an allowed domain
    if netloc not in ALLOWED_CDN_DOMAINS and not any(
        netloc.endswith(f".{allowed}") for allowed in ALLOWED_CDN_DOMAINS
    ):
        raise ValueError(
            f"Disallowed CDN domain: {netloc}. Allowed domains are: "
            f"{', '.join(sorted(ALLOWED_CDN_DOMAINS))}"
        )

    # Reconstruct the URL to ensure consistency
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url