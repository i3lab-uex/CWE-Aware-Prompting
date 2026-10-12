import hmac

# Global dictionary mapping document URLs to their correct cryptographic signatures.
# Example:
# DOCUMENT_SIGNATURES = {
#     "https://example.com/doc1.pdf": "abc123...",
#     ...
# }
DOCUMENT_SIGNATURES = {}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a remote document.

    Args:
        url (str): The URL of the document to validate.
        doc_signature (str): The cryptographic signature provided for verification.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document URL is not found in DOCUMENT_SIGNATURES.
    """
    # Retrieve the expected signature for the given URL
    try:
        expected_signature = DOCUMENT_SIGNATURES[url]
    except KeyError as exc:
        raise IOError(f"Document not found at URL: {url}") from exc

    # Use a constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(doc_signature, expected_signature)