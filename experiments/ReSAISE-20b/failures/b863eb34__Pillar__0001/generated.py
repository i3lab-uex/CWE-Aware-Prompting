import requests
import hmac
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their expected signatures.
# In a real system this would be securely stored and not hard‑coded.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5c2e9b4d8...",
    "https://example.com/doc2.pdf": "f1a7e3c9b0d4...",
    # Add more entries as needed
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature for a remote document matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters:
        doc_url (str): The URL of the document to verify.
        signature (str): The cryptographic signature provided for the document.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        IOError: If the document cannot be accessed (network error, non‑200 status,
                 or any exception during request).
    """
    # Ensure the URL is well‑formed and uses HTTPS to avoid MITM attacks.
    parsed = urlparse(doc_url)
    if parsed.scheme.lower() != "https":
        raise IOError("Insecure URL scheme: only HTTPS is allowed")

    try:
        # Use a short timeout and verify SSL certificates.
        response = requests.get(doc_url, timeout=10, verify=True)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Failed to access document at {doc_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # Unknown document – treat as invalid.
        return False

    # Compare signatures using constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, signature)