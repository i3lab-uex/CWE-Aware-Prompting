import requests
from hmac import compare_digest

# Global dictionary mapping document URLs to their expected cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries (URL : signature)
    "https://example.com/doc1.pdf": "a3f5c8e7b9d2...",
    "https://example.com/doc2.pdf": "f1e3d5c7b9a0...",
    # Add more entries as needed
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a remote document.

    Parameters
    ----------
    doc_link : str
        The URL of the document to validate.
    check_signature : str
        The cryptographic signature that is provided for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature, otherwise False.

    Raises
    ------
    IOError
        If the document at the specified URL cannot be found (HTTP 404).
    """
    # Verify that we have a stored signature for this document
    expected_sig = DOCUMENT_SIGNATURES.get(doc_link)
    if expected_sig is None:
        # No known signature for this URL; treat as missing
        raise IOError(f"Document not found or no stored signature: {doc_link}")

    # Perform a constant‑time comparison to avoid timing attacks
    return compare_digest(expected_sig, check_signature)