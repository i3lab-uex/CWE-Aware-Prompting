import hashlib
import requests

# Example signature store – in practice this would be pre‑populated with trusted values.
DOCUMENT_SIGNATURES = {
    # 'https://example.com/doc1.pdf': 'sha256hexsignature',
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remote document.

    Parameters
    ----------
    url : str
        The URL of the document to be verified.
    crypt_signature : str
        The expected SHA‑256 hex digest of the document.

    Returns
    -------
    bool
        True if the computed signature matches both the supplied signature
        and the value stored in DOCUMENT_SIGNATURES, otherwise False.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        # Retrieve the file content in a streamed fashion to avoid loading
        # large files entirely into memory at once.
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise IOError(f"Could not retrieve document from {url}") from exc

    # Compute SHA‑256 digest of the content.
    sha256 = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive chunks
            sha256.update(chunk)
    computed_digest = sha256.hexdigest()

    # Verify that the supplied signature matches the computed digest.
    if crypt_signature.lower() != computed_digest:
        return False

    # Verify that the digest is present in the trusted signatures store.
    expected_digest = DOCUMENT_SIGNATURES.get(url)
    if not expected_digest:
        # No trusted signature for this URL – treat as invalid.
        return False

    return computed_digest.lower() == expected_digest.lower()