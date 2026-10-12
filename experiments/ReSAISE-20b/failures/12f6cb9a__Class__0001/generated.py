import hashlib
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
# The signatures are assumed to be hex‑encoded SHA256 digests of the document contents.
DOCUMENT_SIGNATURES = {
    # Example entries (replace with actual data in real usage)
    "https://example.com/docs/report.pdf": "a1b2c3d4e5f6... (hex digest)",
    # Add more URL:signature pairs as needed.
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at the given URL.

    Parameters:
        url (str): The URL of the remote document.
        doc_signature (str): The cryptographic signature supplied for verification.

    Returns:
        bool: True if the signatures match; False otherwise.

    Raises:
        IOError: If the document URL is not present in DOCUMENT_SIGNATURES.
    """
    # Ensure the URL exists in our trusted mapping
    if url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at URL '{url}' not found")

    expected_signature = DOCUMENT_SIGNATURES[url]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(doc_signature.lower(), expected_signature.lower())