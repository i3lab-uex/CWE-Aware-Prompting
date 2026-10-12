import hmac

# Example global mapping of document URLs to their correct signatures.
# In a real application this would be populated from a secure source.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # ... other entries ...
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a document identified by `file_url`.

    Parameters:
        file_url (str): The URL of the remote document.
        crypt_signature (str): The signature to validate.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If `file_url` is not present in DOCUMENT_SIGNATURES.
    """
    # Ensure the document URL exists in our signature store
    if file_url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document '{file_url}' not found.")

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES[file_url]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_sig)