import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Predefined mapping of document URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "d41d8cd98f00b204e9800998ecf8427e",
    # "https://example.com/doc2.pdf": "0cc175b9c0f1b6a831c399e269772661",
}

def _fetch_document(url: str) -> bytes:
    """
    Retrieve the document from the given URL.

    Raises:
        IOError: If the document cannot be retrieved.
    """
    try:
        req = Request(url, headers={"User-Agent": "check-file/1.0"})
        with urlopen(req) as response:
            return response.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

def _compute_signature(data: bytes) -> str:
    """
    Compute the SHA-256 hex digest of the document data.
    This is a placeholder; in real scenarios this might be a more
    complex or asymmetric signature verification.
    """
    return hashlib.sha256(data).hexdigest()

def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remote document by checking its cryptographic signature.

    Args:
        document_location (str): URL of the document to verify.
        crypto_sign (str): Signature provided for validation.

    Returns:
        bool: True if the signature matches the authentic one, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    # Retrieve the document to ensure it exists and is accessible
    data = _fetch_document(document_location)

    # Compute the expected signature (e.g., SHA-256 hash of the content)
    computed_sig = _compute_signature(data)

    # Retrieve the authentic signature from the pre-defined dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(document_location)

    # If no signature is stored for this URL, treat as invalid
    if expected_sig is None:
        return False

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(computed_sig, expected_sig):
        return False

    # Finally compare the provided signature with the computed one
    return hmac.compare_digest(crypto_sign, computed_sig)