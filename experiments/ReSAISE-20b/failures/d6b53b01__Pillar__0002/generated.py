import hashlib
import urllib.request
import ssl

# Example dictionary of valid signatures (URL -> SHA256 hex digest)
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "a3b5c7d9...",
    # Add real entries here
}


def _fetch_document(url: str) -> bytes:
    """
    Retrieve the raw content of a remote document.
    Raises IOError if the request fails or returns non‑200 status.
    """
    try:
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, timeout=10, context=context) as resp:
            if resp.status != 200:
                raise IOError(f"HTTP error {resp.status} retrieving {url}")
            return resp.read()
    except Exception as exc:
        raise IOError(f"Could not retrieve document from {url}") from exc


def _compute_sha256(data: bytes) -> str:
    """
    Compute the SHA‑256 hex digest of the given data.
    """
    return hashlib.sha256(data).hexdigest()


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate a remote document against its expected cryptographic signature.

    Parameters
    ----------
    document_location : str
        URL of the remote document to be validated.
    crypto_sign : str
        The signature value provided for validation.

    Returns
    -------
    bool
        True if the document's computed signature matches both the stored
        and provided signatures; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # 1. Retrieve the document
    data = _fetch_document(document_location)

    # 2. Compute local SHA‑256 digest
    computed_digest = _compute_sha256(data)

    # 3. Fetch the expected signature from the dictionary
    expected_digest = DOCUMENT_SIGNATURES.get(document_location)
    if expected_digest is None:
        # If no stored signature, treat as failure (but do not raise)
        return False

    # 4. Compare all three values
    if computed_digest.lower() == expected_digest.lower() and \
       computed_digest.lower() == crypto_sign.lower():
        return True

    return False