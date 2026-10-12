import urllib.request
import urllib.error
import hmac

# Global dictionary mapping resource URLs to their expected cryptographic signatures.
DOC_HASHES = {
    # Example entries (these should be replaced with real URLs and signatures)
    "https://example.com/doc1.pdf": "a3f5e2c8b4d6e7f9...",
    "https://example.com/doc2.pdf": "b1c4d6e8f0a2b3c5...",
    # Add more entries as needed
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at `resource_url`.

    Parameters:
        resource_url (str): The URL of the remote document.
        crypto_signature (str): The signature supplied for verification.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        IOError: If the document cannot be accessed at the given URL.
    """
    # 1. Verify that we can reach the resource
    try:
        with urllib.request.urlopen(resource_url, timeout=10) as response:
            # We don't need the content; we just want to confirm accessibility.
            if response.status != 200:
                raise urllib.error.HTTPError(
                    resource_url,
                    response.status,
                    f"Unexpected HTTP status {response.status}",
                    response.headers,
                    None
                )
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        # Wrap the underlying exception in an IOError for consistency
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # 2. Retrieve the expected signature for this URL
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # No known signature for this resource; treat as invalid
        return False

    # 3. Perform a constant‑time comparison to mitigate timing attacks
    try:
        match = hmac.compare_digest(expected_sig, crypto_signature)
    except TypeError:
        # In case signatures are not byte strings; convert to bytes safely
        match = hmac.compare_digest(
            expected_sig.encode('utf-8'), crypto_signature.encode('utf-8')
        )

    return match