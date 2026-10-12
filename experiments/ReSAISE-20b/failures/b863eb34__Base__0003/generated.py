import requests
from hmac import compare_digest

# Global dictionary mapping document URLs to their expected signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    "https://example.com/docs/report.pdf": "abcd1234efgh5678ijkl9012mnop3456",
    # Add more URL:signature pairs as needed.
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature for a remote document matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters:
        doc_url (str): URL of the document to verify.
        signature (str): Cryptographic signature provided for the document.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        IOError: If the document cannot be accessed at the given URL.
    """
    # Ensure we can access the document to confirm its availability
    try:
        response = requests.head(doc_url, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # Retrieve the expected signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If there is no stored signature, consider verification failed
    if expected_sig is None:
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return compare_digest(signature, expected_sig)