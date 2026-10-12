import hmac

# Global mapping of document URLs to their correct cryptographic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries – in real use these would be actual URLs and signatures.
    "https://example.com/doc1.pdf": "a3f5c9e8b2d4... (hex)",
    "https://example.com/doc2.pdf": "c1b7e4d9f6a8... (hex)",
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the document identified by `file_url`.

    Parameters:
        file_url (str): The URL of the document to validate.
        crypt_signature (str): The signature supplied for verification.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If `file_url` is not present in DOCUMENT_SIGNATURES.
    """
    # Ensure the document URL exists in our registry
    if file_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at URL '{file_url}' could not be found.")

    # Retrieve the expected signature
    expected_signature = DOCUMENT_SIGNATURES[file_url]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(crypt_signature, expected_signature)