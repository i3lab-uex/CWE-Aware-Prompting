#!/usr/bin/env python3
"""
Utility to validate cryptographic signatures for remote documents.
"""

import requests
from hmac import compare_digest
from urllib.parse import urlparse, unquote

# Global mapping of document URLs to their expected signatures.
DOC_SIGNATURES = {
    # Example entries:
    # "https://example.com/docs/report.pdf": "sha256:abcd1234...",
    # Add actual URL → signature mappings here.
}


def _is_url_accessible(url: str) -> bool:
    """
    Perform a lightweight HEAD request to confirm that the URL is reachable.
    Returns True if the response status code is 200-399, otherwise False.
    """
    try:
        # Use a short timeout to avoid hanging on bad hosts
        resp = requests.head(url, allow_redirects=True, timeout=5)
        return 200 <= resp.status_code < 400
    except (requests.RequestException, requests.Timeout):
        return False


def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for the document located at *file_url*.

    Parameters
    ----------
    file_url : str
        URL of the document to validate.
    sign : str
        Cryptographic signature supplied by the caller.

    Returns
    -------
    bool
        True if *sign* matches the expected signature; False otherwise.

    Raises
    ------
    IOError
        If the document at *file_url* is inaccessible (e.g., network error,
        non-2xx/3xx HTTP status, or timeout).
    """
    # Ensure the URL is reachable before any further checks.
    if not _is_url_accessible(file_url):
        raise IOError(f"Document at {file_url!r} is inaccessible")

    # Normalise the URL to use as a key in DOC_SIGNATURES.
    parsed = urlparse(file_url)
    normalized_path = unquote(parsed.path)
    key = f"{parsed.scheme}://{parsed.netloc}{normalized_path}"

    expected_sig = DOC_SIGNATURES.get(key)
    if expected_sig is None:
        # No known signature for this document; treat as invalid.
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return compare_digest(sign, expected_sig)


# Example usage (uncomment for testing):
# if __name__ == "__main__":
#     try:
#         result = validate_document(
#             "https://example.com/docs/report.pdf",
#             "sha256:abcd1234..."
#         )
#         print("Signature valid:", result)
#     except IOError as exc:
#         print("Error accessing document:", exc)