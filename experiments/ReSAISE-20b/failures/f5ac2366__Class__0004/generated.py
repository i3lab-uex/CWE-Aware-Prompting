import urllib.parse

# Define the set of allowed CDN domains.  In a real application this would be
# loaded from configuration or environment variables.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.example.org",
    "static.myapp.net",
}

def construct_external_resource_url(cdn_base_url: str, resource_id: str, resource_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN, e.g. "https://cdn.example.com/".
    resource_id : str
        The unique identifier of the requested resource.  This value is used
        verbatim in the path component; callers should ensure it does not
        contain dangerous characters (e.g. "../").
    resource_type : str
        The type of resource, e.g. "image", "script".  It is inserted as a
        sub‑directory in the URL.

    Returns
    -------
    str
        The fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the constructed URL resolves to a domain that is not in
        ``ALLOWED_CDN_DOMAINS``.
    """
    # Normalise the base URL and ensure it ends with a slash
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base_url!r}")

    # Validate the domain against the whitelist
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Domain {parsed_base.netloc!r} is not an allowed CDN domain")

    # Build the relative path.  ``urllib.parse.quote`` ensures that any
    # characters in resource_id or resource_type are safely percent‑encoded.
    safe_resource_id = urllib.parse.quote(resource_id, safe="")
    safe_resource_type = urllib.parse.quote(resource_type, safe="")

    # Construct the final path.  We intentionally avoid any leading ".."
    # sequences by not allowing them in ``resource_id`` or ``resource_type``
    # and by normalising the path with `os.path.normpath`.
    relative_path = f"{safe_resource_type}/{safe_resource_id}"
    # ``urljoin`` will correctly handle the trailing slash in the base URL.
    full_url = urllib.parse.urljoin(parsed_base.geturl() + "/", relative_path)

    # Re‑parse the final URL to double‑check the domain
    parsed_final = urllib.parse.urlparse(full_url)
    if parsed_final.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Constructed URL points to disallowed domain: {parsed_final.netloc!r}")

    return full_url