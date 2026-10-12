import urllib.parse

# Example allowed CDN domains – replace with your real list
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.myapp.net",
    "static.somecdn.org",
}

def generate_external_resource_link(cdn_host_url: str,
                                     resource_tag: str,
                                     resource_category: str) -> str:
    """
    Construct a full URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_host_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_tag : str
        Unique identifier for the requested resource.
    resource_category : str
        Type/category of the resource, e.g. "image" or "script".

    Returns
    -------
    str
        The fully qualified URL pointing to the resource.

    Raises
    ------
    ValueError
        If the CDN domain is not in ``ALLOWED_CDN_DOMAINS`` or if the
        constructed URL would point outside of an allowed domain.
    """
    # Parse the base CDN URL
    parsed_base = urllib.parse.urlparse(cdn_host_url)

    # Ensure the scheme is present; default to https if missing
    scheme = parsed_base.scheme or "https"

    # Validate the CDN domain
    netloc = parsed_base.netloc
    if not netloc:
        # The URL might have been provided without scheme, e.g. "cdn.example.com"
        netloc = parsed_base.path
    if not netloc:
        raise ValueError("Invalid CDN host URL: missing domain")

    # Normalize the domain (strip port if present)
    domain = netloc.split(":")[0]
    if domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"CDN domain '{domain}' is not allowed")

    # Safely encode path components
    safe_category = urllib.parse.quote(resource_category.strip("/"))
    safe_tag = urllib.parse.quote(resource_tag.strip("/"))

    # Construct the path; ensure a single leading slash
    path = f"/{safe_category}/{safe_tag}"

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (scheme, netloc, path, "", "", "")
    )

    # Final safety check: ensure the resulting URL's netloc is still allowed
    final_parsed = urllib.parse.urlparse(final_url)
    final_domain = final_parsed.netloc.split(":")[0]
    if final_domain not in ALLOWED_CDN_DOMAINS:
        raise ValueError("Constructed URL points to an unauthorized domain")

    return final_url