import urllib.request
import hmac

# Global dictionary containing the correct signatures for known documents.
DOCUMENT_SIGNATURES = {
    # Example entries (URL: signature)
    "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    "https://example.com/doc2.pdf": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed.
}


def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given document URL.

    Parameters:
        doc_link (str): The URL of the document to validate.
        check_signature (str): The cryptographic signature provided for verification.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        IOError: If the document URL is not found in DOCUMENT_SIGNATURES.
    """
    # Ensure we only accept URLs that are present in our signature store.
    if doc_link not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at {doc_link} cannot be found or is not registered.")

    # Retrieve the stored signature for this document.
    expected_signature = DOCUMENT_SIGNATURES[doc_link]

    # Perform a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, check_signature)