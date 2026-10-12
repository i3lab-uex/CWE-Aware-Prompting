import hashlib
import urllib.request
import urllib.error

# Pre‑defined dictionary mapping document URLs to their trusted signatures.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.pdf": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "https://example.com/doc2.txt": "5d41402abc4b2a76b9719d911017c592",
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its cryptographic
    signature with the expected value.

    Args:
        url: The URL of the document to fetch.
        crypt_signature: The expected signature (hex string) for the content.

    Returns:
        True if the computed signature matches the expected one, False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

    # Compute SHA-256 hash of the retrieved data
    computed_hash = hashlib.sha256(data).hexdigest()

    # Compare with both the supplied signature and the trusted signature from
    # DOCUMENT_SIGNATURES (if present). The function returns True only if
    # both match the computed hash.
    trusted_sig = DOCUMENT_SIGNATURES.get(url)
    if trusted_sig and computed_hash != trusted_sig:
        return False

    return computed_hash == crypt_signature