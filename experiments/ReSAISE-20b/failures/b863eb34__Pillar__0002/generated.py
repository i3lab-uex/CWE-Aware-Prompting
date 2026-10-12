import hashlib
import hmac
import requests

# Global dictionary mapping document URLs to their correct signatures (hex strings)
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "3f2a8c9e... (hex signature)",
    "https://example.com/doc2.pdf": "a1b2c3d4... (hex signature)",
}

def _download_document(url: str) -> bytes:
    """
    Download the document from `url`. Raises IOError if the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, ValueError) as exc:
        raise IOError(f"Unable to access document at {url}") from exc
    return response.content

def _compute_signature(content: bytes) -> str:
    """
    Compute the SHA-256 hex digest of `content`. This mimics the signature
    generation algorithm used for DOCUMENT_SIGNATURES.
    """
    return hashlib.sha256(content).hexdigest()

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at `doc_url` matches the provided `signature`.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature (hex string) supplied for the document.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed at the given URL.
    """
    # 1. Ensure we can access the document
    content = _download_document(doc_url)

    # 2. Compute the signature locally (using the same algorithm as
    #    DOCUMENT_SIGNATURES). In a real system, the signature might be
    #    produced by a private key; here we simply hash for illustration.
    local_sig = _compute_signature(content)

    # 3. Compare the signatures in constant time to avoid timing attacks.
    return hmac.compare_digest(local_sig.lower(), signature.lower())