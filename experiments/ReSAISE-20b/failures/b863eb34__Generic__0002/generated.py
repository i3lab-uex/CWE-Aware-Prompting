import hashlib
import requests
from typing import Dict

# Global dictionary mapping document URLs to their expected SHA256 signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries:
    # "https://example.com/doc1.pdf": "3a7bd3e2360a... (hex signature)",
    # "https://example.com/doc2.txt": "b1d2f4c3e6a9... (hex signature)",
}

def _compute_sha256(content: bytes) -> str:
    """Return the hex digest of the SHA256 hash of *content*."""
    sha = hashlib.sha256()
    sha.update(content)
    return sha.hexdigest()

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at *doc_url* matches the expected cryptographic
    signature.

    Parameters:
        doc_url (str): URL of the remote document.
        signature (str): Signature supplied by caller.

    Returns:
        bool: True if the document's SHA256 matches the expected signature,
              False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from *doc_url*.
    """
    try:
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # Compute SHA256 of the retrieved content.
    actual_sig = _compute_sha256(response.content)

    # Compare with expected signature from the global dictionary.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If no entry exists, treat as invalid.
    if expected_sig is None:
        return False

    # Constant-time comparison to mitigate timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    # Compare provided signature with expected and actual.
    if not _constant_time_compare(signature.lower(), expected_sig.lower()):
        return False

    # Additionally ensure the actual content matches the expected signature.
    return _constant_time_compare(actual_sig, expected_sig)