import urllib.parse

# Set of CDN domains that are considered safe.
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.org",
    "static.somecdn.net",
}

def create_external_resource_link(cdn_url: str, res_id: str, res_type: str) -> str:
    """
    Assemble a validated URL for an external resource.

    Parameters
    ----------
    cdn_url : str
        Base CDN URL, e.g. "https://cdn.example.com".
    res_id : str
        Unique identifier of the resource.
    res_type : str
        Type/category of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        Fully-qualified, validated URL to the requested resource.

    Raises
    ------
    ValueError
        If the resolved CDN domain is not in ``ALLOWED_CDN_DOMAINS``.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_url)

    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN URL: {cdn_url!r}")

    # Ensure the base URL does not contain a path or query component
    if parsed_base.path not in ("", "/"):
        raise ValueError(f"CDN URL must not contain a path: {cdn_url!r}")

    # Canonicalize the domain (lowercase, strip port if present)
    netloc = parsed_base.netloc.split(":")[0].lower()
    if netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Unauthorized CDN domain: {netloc!r}")

    # Build the resource path safely
    # Use quote to escape any special characters in res_id and res_type
    safe_res_type = urllib.parse.quote(res_type.strip(), safe="")
    safe_res_id = urllib.parse.quote(res_id.strip(), safe="")

    resource_path = f"/{safe_res_type}/{safe_res_id}"

    # Construct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return final_url