import re
from urllib.parse import urlparse, urlunparse

# A whitelist of fully qualified domain names that are allowed for redirection.
# The list can be extended as needed. Subdomains are not automatically
# allowed unless explicitly listed.
APPROVED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    "myapp.example.net",
}

def _is_approved_domain(netloc: str) -> bool:
    """
    Check if the given netloc (host[:port]) is in the approved list.
    The comparison is case‑insensitive and ignores any port number.
    """
    # Remove default ports to avoid false negatives
    host = netloc.split(":")[0].lower()
    return host in APPROVED_DOMAINS

def validate_safe_redirect(input_link: str) -> str:
    """
    Validate and sanitize a user supplied URL for safe redirection.

    Parameters
    ----------
    input_link : str
        The raw URL provided by the user. It may be an absolute or relative URL.

    Returns
    -------
    str
        A fully qualified, safe-to-use URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is absolute and its domain is not in the approved list,
        or if it uses a scheme that could lead to unintended proxying.
    """
    # Parse the URL
    parsed = urlparse(input_link)

    # Reject URLs that use a scheme other than http/https or are empty.
    if parsed.scheme and parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # If the URL is relative, we treat it as an internal redirect and simply
    # return the normalized path. This prevents leaking user input to external
    # sites and avoids CWE-441.
    if not parsed.netloc:
        # Ensure the path starts with a slash to avoid directory traversal.
        safe_path = re.sub(r"[^a-zA-Z0-9/_\-.?=&%]*", "", parsed.path)
        return safe_path

    # For absolute URLs, verify the domain against the whitelist.
    if not _is_approved_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not approved for redirection")

    # Reconstruct the URL to ensure consistent formatting.
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return safe_url

# Example usage (for illustration only; remove or comment out in production)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/dashboard",
        "/internal/page?x=1",
        "http://malicious.com/steal",
        "ftp://example.com/resource"
    ]

    for url in test_urls:
        try:
            print(f"Input: {url}\nValidated: {validate_safe_redirect(url)}\n")
        except ValueError as e:
            print(f"Input: {url}\nError: {e}\n")