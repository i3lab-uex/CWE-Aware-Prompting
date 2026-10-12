import re
from urllib.parse import urlparse, urlunparse

# A list of trusted domains (you can extend this as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "storage.googleapis.com",
    "imgur.com",  # include root domain
}

# Regex to validate that the URL uses http or https scheme only
_SCHEME_REGEX = re.compile(r"^(https?)$", re.IGNORECASE)


def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL belongs to a trusted provider.

    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        The validated and canonicalized URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed = urlparse(img_src)

    # 1. Scheme validation
    if not _SCHEME_REGEX.match(parsed.scheme):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed.")

    # 2. Domain validation
    hostname = parsed.hostname or ""
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS):
        raise ValueError(f"Untrusted domain '{hostname}'. Allowed domains: {', '.join(TRUSTED_DOMAINS)}")

    # 3. Reconstruct the URL to ensure consistency (e.g., no fragments, proper percent‑encoding)
    # Preserve path, params, query but drop fragment
    canonical = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            "",  # no fragment
        )
    )

    return canonical


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         print(validate_image_source("https://i.imgur.com/abcd1234.jpg"))
#     except ValueError as e:
#         print(e)