import urllib.parse

# Example allowed CDN domains (modify as needed)
ALLOWED_CDN_DOMAINS = {"cdn.example.com", "assets.myapp.net"}


def construct_external_resource_url(cdn_base_url: str, resource_id: str,
                                     resource_type: str) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        The base URL of the CDN (e.g., "https://cdn.example.com/").
    resource_id : str
        Identifier of the requested resource (e.g., "logo.png").
    resource_type : str
        Type of resource. Accepted values are 'image', 'script', or any other
        custom category that the CDN uses in its path structure.

    Returns
    -------
    str
        A fully-qualified URL that points to the requested resource on a CDN.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to a domain listed in
        ``ALLOWED_CDN_DOMAINS`` or if the input parameters are invalid.
    """
    # Validate inputs
    if not cdn_base_url or not resource_id or not resource_type:
        raise ValueError("All arguments must be non-empty strings")

    # Sanitize resource_id: strip leading/trailing slashes and disallow '..'
    sanitized_id = resource_id.strip("/")
    if ".." in sanitized_id or "/" in sanitized_id:
        raise ValueError("Invalid resource identifier")

    # Encode the ID to be URL safe
    encoded_id = urllib.parse.quote(sanitized_id)

    # Build the path based on resource_type
    # e.g., /images/logo.png or /scripts/app.js
    path = urllib.parse.urljoin(
        f"/{resource_type.rstrip('/')}/", encoded_id
    )

    # Construct the final URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid CDN base URL")

    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    # Ensure the final URL points to an allowed CDN domain
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(f"Disallowed CDN domain: {parsed_base.netloc}")

    return final_url