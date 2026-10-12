import hmac
from typing import Dict

# A global mapping from document URLs to their expected cryptographic signatures.
# In a real system this would be securely stored and accessed.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real URLs and signatures.
    "https://example.com/doc1.pdf": "a3f5c8d2e7b9...",
    "https://example.com/doc2.pdf": "4c1d6e9f3a8b...",
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    signature for a document located at `url`.

    Parameters:
        url (str): The URL of the remote document.
        doc_signature (str): The signature supplied for verification.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document at `url` cannot be found.
    """
    # Ensure input types are correct
    if not isinstance(url, str) or not isinstance(doc_signature, str):
        raise TypeError("Both url and doc_signature must be strings")

    # Retrieve the expected signature from the global store
    expected_sig = DOCUMENT_SIGNATURES.get(url)

    if expected_sig is None:
        # The document's signature is not known; treat as missing
        raise IOError(f"Document at {url} not found in signature store")

    # Perform a constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, doc_signature)