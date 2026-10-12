import requests
import hmac

# Global dictionary mapping document URLs to their expected signatures.
DOCUMENT_SIGNATURES = {
    # Example entries; replace with real data as needed
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature for a document matches the expected
    value stored in DOCUMENT_SIGNATURES.

    Parameters:
        doc_url (str): The URL of the document to verify.
        signature (str): The cryptographic signature provided for the document.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        IOError: If the document cannot be accessed at the given URL.
    """
    # Check that the URL is reachable before attempting signature verification.
    try:
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Treat any network or HTTP error as an inability to access the document.
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # Retrieve the expected signature for this URL.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    if expected_sig is None:
        # No known signature for this document; treat as invalid.
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE-693).
    return hmac.compare_digest(signature, expected_sig)