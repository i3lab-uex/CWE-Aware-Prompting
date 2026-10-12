import hashlib
import hmac
from urllib.parse import urlparse

import requests


# Global dictionary mapping URLs to their correct cryptographic signatures
DOCUMENT_SIGNATURES = {
    # Example entries; replace with actual data in production.
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # ... more entries ...
}


def _get_document_signature(url: str) -> str:
    """
    Retrieve the expected signature for a given URL from DOCUMENT_SIGNATURES.
    Raises KeyError if the URL is not present in the mapping.
    """
    return DOCUMENT_SIGNATURES[url]


def _url_exists(url: str) -> bool:
    """
    Perform a lightweight HEAD request to confirm the document exists.
    Raises IOError if the URL cannot be reached or returns a non-success status code.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code == 404:
            raise IOError(f"Document not found: {url}")
        # Treat any non-success status as an error for safety
        if not response.ok:
            raise IOError(f"Failed to access {url}: HTTP {response.status_code}")
        return True
    except requests.RequestException as exc:
        raise IOError(f"Error accessing {url}: {exc}") from exc


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a document located at file_url.

    Parameters:
        file_url (str): URL of the remote document.
        crypt_signature (str): Signature supplied for verification.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        IOError: If the document cannot be found or accessed.
    """
    # Ensure the URL is syntactically valid
    parsed = urlparse(file_url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError(f"Invalid URL: {file_url}")

    # Check that the document exists
    _url_exists(file_url)

    try:
        expected_sig = _get_document_signature(file_url)
    except KeyError as exc:
        raise IOError(f"No stored signature for URL: {file_url}") from exc

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_sig, crypt_signature)