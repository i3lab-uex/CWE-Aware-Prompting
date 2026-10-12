import hmac

# Global dictionary mapping document URLs to their correct signatures.
# In a real system this would be securely stored and managed.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef1234",
    # Add more URLs and signatures as needed
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document located at the given URL.

    Args:
        url: The URL of the document to validate.
        doc_signature: The cryptographic signature supplied for verification.

    Returns:
        True if the signature matches the stored one, False otherwise.

    Raises:
        IOError: If the document URL is not present in DOCUMENT_SIGNATURES.
    """
    # Ensure the URL exists in our signature store
    if url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at URL '{url}' could not be found.")

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES[url]

    # Use a constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, doc_signature)