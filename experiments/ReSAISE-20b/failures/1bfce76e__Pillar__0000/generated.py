import urllib.parse

# Predefined set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "static.myapp.org",
    "assets.content.net",
}

def generate_external_resource_url(cdn_base: str, res_id: str, res_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base : str
        Base URL of the CDN (e.g. "https://cdn.example.com").
    res_id : str
        Identifier of the resource (e.g. "12345.png").
    res_type : str
        Type of resource, used as a path segment (e.g. "image", "script").

    Returns
    -------
    str
        The absolute URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resolved URL does not target an allowed CDN domain.
    """
    # Parse the base URL to extract components
    parsed_base = urllib.parse.urlparse(cdn_base)

    # Ensure the base URL has a scheme and network location
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base!r}")

    # Validate that the CDN domain is allowed
    if parsed_base.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"CDN domain {parsed_base.netloc!r} is not in the allowed list"
        )

    # Sanitize path components to prevent directory traversal or injection
    safe_res_type = urllib.parse.quote(res_type.strip(), safe="")
    safe_res_id = urllib.parse.quote(res_id.strip(), safe="")

    # Construct the relative path; ensure it starts with a single slash
    relative_path = f"/{safe_res_type}/{safe_res_id}"

    # Combine base URL with the relative path
    full_url = urllib.parse.urljoin(cdn_base.rstrip("/") + "/", relative_path.lstrip("/"))

    # Final validation: ensure the resulting URL still points to an allowed domain
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.netloc.lower() not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Constructed URL points to disallowed domain: {final_parsed.netloc!r}"
        )

    return full_url