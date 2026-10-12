import requests
import hmac

# Global dictionary that maps document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    # Example entries – in a real system these would be securely stored.
    "https://example.com/doc1.pdf": "a3f5c9b8e2d4...",
    "https://example.com/doc2.pdf": "7e1a9c3d4f6b...",
    # Add more entries as needed.
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document located at `doc_link`.

    Parameters
    ----------
    doc_link : str
        URL of the document to validate.
    check_signature : str
        Signature supplied for verification.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be found (HTTP 404) or if the request fails.
    """
    # Verify that the document exists before checking the signature.
    try:
        response = requests.head(doc_link, timeout=10)
        if response.status_code == 404:
            raise IOError(f"Document not found: {doc_link}")
        response.raise_for_status()
    except requests.RequestException as exc:
        raise IOError(f"Failed to access document at {doc_link}: {exc}") from exc

    # Retrieve the expected signature for this URL.
    expected_signature = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_signature is None:
        # If we have no stored signature, treat it as a mismatch.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(expected_signature, check_signature)