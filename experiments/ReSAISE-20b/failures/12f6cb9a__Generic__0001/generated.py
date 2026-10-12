import hmac

# Example mapping of document URLs to their correct cryptographic signatures.
# In a real system this would be securely stored and managed.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5c9b2e8d7...",
    "https://example.com/doc2.pdf": "4f6b1e9d3a12...",
    # ... add more entries as needed
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document located at `url`.

    Parameters:
        url (str): The URL of the remote document.
        doc_signature (str): The signature to verify.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If no signature is stored for the given URL.
    """
    # Retrieve the expected signature for the document
    expected_signature = DOCUMENT_SIGNATURES.get(url)

    if expected_signature is None:
        raise IOError(f"Document at URL '{url}' not found in signature store.")

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, doc_signature)