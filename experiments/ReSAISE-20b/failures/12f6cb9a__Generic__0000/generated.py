import hmac

# Example global mapping of URLs to their correct signatures.
# In a real application this would be securely loaded from a trusted source.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef",
    # ... more entries ...
}


def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document at the given URL.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If no signature is found for the given URL (i.e., document not known).
    """
    # Retrieve the expected signature from the global mapping.
    expected_sig = DOCUMENT_SIGNATURES.get(url)

    if expected_sig is None:
        # No record for this URL; treat as missing document.
        raise IOError(f"Document not found or signature missing for URL: {url}")

    # Use a timing‑safe comparison to prevent timing attacks.
    return hmac.compare_digest(expected_sig, doc_signature)