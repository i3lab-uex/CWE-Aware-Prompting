import hmac

# Global dictionary mapping document URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/docs/report.pdf": "a1b2c3d4e5f6",
    "https://example.com/docs/terms.txt":  "1234567890abcdef",
    # Add more entries as needed
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document identified by its URL.

    Args:
        file_url (str): The URL of the document to validate.
        crypt_signature (str): The signature provided for verification.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If the document URL is not present in DOCUMENT_SIGNATURES.
    """
    # Ensure the document exists in our signature store
    if file_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document '{file_url}' not found.")

    # Retrieve the stored signature
    expected_signature = DOCUMENT_SIGNATURES[file_url]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypt_signature)