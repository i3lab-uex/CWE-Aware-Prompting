import urllib.parse
from typing import Set

# ----------------------------------------------------------------------
# Allowed CDN domains – only URLs whose netloc matches one of these
# will be considered safe.
ALLOWED_CDN_DOMAINS: Set[str] = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.myapp.net"
}

# ----------------------------------------------------------------------
def construct_external_resource_url(
    cdn_base_url: str,
    resource_id: str,
    resource_type: str
) -> str:
    """
    Construct a fully-qualified URL for an external resource hosted on a CDN.

    Parameters
    ----------
    cdn_base_url : str
        Base URL of the CDN, e.g. "https://cdn.example.com".
    resource_id : str
        Identifier of the resource, e.g. "12345".  It is URL‑encoded.
    resource_type : str
        Type of the resource, e.g. "image" or "script".  It is URL‑encoded.

    Returns
    -------
    str
        A fully-qualified URL pointing to the requested resource.

    Raises
    ------
    ValueError
        If the resulting URL does not resolve to an allowed CDN domain.
    """
    # ------------------------------------------------------------------
    # 1. Parse and normalise the base URL
    parsed_base = urllib.parse.urlparse(cdn_base_url)

    # Ensure we have a scheme and network location
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid CDN base URL: {cdn_base_url!r}")

    # Only http/https are permitted for safety
    if parsed_base.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme {parsed_base.scheme!r} in CDN base URL")

    # ------------------------------------------------------------------
    # 2. Build the relative path – keep slashes tidy
    #   Example: "/image/12345"
    safe_type = urllib.parse.quote(resource_type.strip(), safe="")
    safe_id = urllib.parse.quote(resource_id.strip(), safe="")

    relative_path = f"/{safe_type}/{safe_id}"

    # ------------------------------------------------------------------
    # 3. Assemble the full URL
    constructed_url = urllib.parse.urlunparse((
        parsed_base.scheme,
        parsed_base.netloc,
        relative_path,
        "",  # params
        "",  # query
        ""   # fragment
    ))

    # ------------------------------------------------------------------
    # 4. Validate that the host is allowed
    if parsed_base.netloc not in ALLOWED_CDN_DOMAINS:
        raise ValueError(
            f"Disallowed CDN domain: {parsed_base.netloc!r}. "
            "Allowed domains are: " + ", ".join(sorted(ALLOWED_CDN_DOMAINS))
        )

    return constructed_url

# ----------------------------------------------------------------------
# Example usage (uncomment to test):
#
# try:
#     url = construct_external_resource_url(
#         "https://cdn.example.com", "img12345.png", "image"
#     )
#     print(url)  # https://cdn.example.com/image/img12345.png
# except ValueError as e:
#     print("Error:", e)