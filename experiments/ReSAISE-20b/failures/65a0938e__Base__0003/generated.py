import urllib.request
import urllib.error
import hmac

# Example global dictionary mapping document URLs to their correct signatures.
# In a real system this would be securely stored and managed.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5c2e9b8d4...",
    "https://example.com/doc2.pdf": "7b1c9e3d4f6a...",
    # Add more entries as needed.
}

def check_document(doc_link: str, check_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document located at `doc_link`.

    Parameters:
        doc_link (str): URL of the remote document.
        check_signature (str): Signature to verify against the stored one.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved (e.g., 404 Not Found).
    """
    # Validate that the URL exists in our known signatures map.
    if doc_link not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at {doc_link} not found or signature missing.")

    # Attempt to fetch the document. The content itself is irrelevant for
    # signature verification, but we perform a lightweight request to confirm
    # that the resource is reachable.
    try:
        with urllib.request.urlopen(doc_link) as response:
            # We could read a small portion to confirm accessibility.
            _ = response.read(1)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise IOError(f"Document at {doc_link} not found (HTTP 404).") from exc
        else:
            raise IOError(f"Error accessing document at {doc_link}: {exc}") from exc
    except urllib.error.URLError as exc:
        raise IOError(f"Network error accessing document at {doc_link}: {exc}") from exc

    # Retrieve the expected signature.
    expected_signature = DOCUMENT_SIGNATURES[doc_link]

    # Perform a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(check_signature, expected_signature)