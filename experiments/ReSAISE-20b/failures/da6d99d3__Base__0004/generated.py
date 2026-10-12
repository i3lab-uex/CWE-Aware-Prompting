import urllib.parse

# Predefined set of safe CDN domains (example values)
ALLOWED_CDN_DOMAINS = {
    "cdn.example.com",
    "assets.safe-cdn.org",
    "static.secure.net",
}

def build_external_resource_link(cdn_url: str, resource_key: str, res_category: str) -> str:
    """
    Construct a URL that points to an external resource on a trusted CDN.

    Parameters
    ----------
    cdn_url : str
        Base URL of the CDN (e.g., "https://cdn.example.com").
    resource_key : str
        Identifier for the specific resource (e.g., "logo.png").
    res_category : str
        Category of the resource, used as a sub‑directory (e.g., "image").

    Returns
    -------
    str
        The fully resolved URL.

    Raises
    ------
    ValueError
        If the CDN domain is not in ALLOWED_CDN_DOMAINS or if any part of
        the URL would cause a redirect to an untrusted domain.
    """
    # Parse and validate the base CDN URL
    parsed_cdn = urllib.parse.urlparse(cdn_url)

    if parsed_cdn.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed_cdn.scheme}")

    # Ensure the domain is explicitly allowed
    netloc = parsed_cdn.netloc.lower()
    if not any(netloc == domain or netloc.endswith("." + domain) for domain in ALLOWED_CDN_DOMAINS):
        raise ValueError(f"Disallowed CDN domain: {netloc}")

    # Normalise the path components to avoid traversal attacks
    # Strip leading/trailing slashes and collapse multiple separators
    def safe_join(*parts: str) -> str:
        cleaned = "/".join(part.strip("/") for part in parts if part)
        return urllib.parse.quote(cleaned, safe="/")

    # Build the path: /{res_category}/{resource_key}
    resource_path = safe_join(parsed_cdn.path, res_category, resource_key)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_cdn.scheme,
            netloc,
            resource_path,
            "",  # params
            "",  # query
            "",  # fragment
        )
    )

    return final_url


# Example usage:
if __name__ == "__main__":
    try:
        url = build_external_resource_link(
            "https://cdn.example.com/assets",
            "logo.png",
            "image"
        )
        print(url)  # https://cdn.example.com/assets/image/logo.png
    except ValueError as e:
        print(f"Invalid CDN URL: {e}")