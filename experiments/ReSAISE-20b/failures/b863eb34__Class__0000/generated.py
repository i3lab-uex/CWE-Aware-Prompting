import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Global mapping of document URLs to their expected SHA‑256 signatures
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "3a7bd3e2360a5d9b2f...",
    # "https://example.com/doc2.txt": "1c8e5d4f9b6a..."
}


def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document located at `doc_url` has a SHA‑256 hash matching
    the provided `signature`.

    Parameters:
        doc_url (str): The URL of the document to retrieve.
        signature (str): Expected hexadecimal SHA‑256 hash of the document.

    Returns:
        bool: True if the computed hash matches `signature`, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    try:
        # Retrieve the document as bytes
        req = Request(doc_url, headers={"User-Agent": "verify-document/1.0"})
        with urlopen(req, timeout=10) as resp:
            content = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Could not access document at {doc_url}") from exc

    # Compute SHA‑256 hash of the retrieved content
    computed_hash = hashlib.sha256(content).hexdigest()

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed_hash, signature.lower())