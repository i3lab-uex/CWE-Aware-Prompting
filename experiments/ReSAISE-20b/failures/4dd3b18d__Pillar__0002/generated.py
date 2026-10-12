import urllib.request
import urllib.error
import hmac
from pathlib import Path

# Example global mapping of document identifiers to expected signatures.
# In real code this would be populated from a secure source.
DOC_SIGNATURES = {
    "doc1.pdf": b"5f4dcc3b5aa765d61d8327deb882cf99",
    "doc2.pdf": b"6c569aabbf7775ef8fc570e228c16b98",
    # ...
}

def _extract_doc_id(url: str) -> str:
    """
    Extract the document identifier from a URL.
    This implementation assumes that the last path component is the file name.
    """
    return Path(urllib.parse.urlparse(url).path).name

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate a cryptographic signature against the expected value for a document.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` is inaccessible.
    """
    # 1. Verify that the remote resource can be accessed
    try:
        with urllib.request.urlopen(file_url, timeout=10) as resp:
            # Just read a small amount to confirm accessibility.
            resp.read(1)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        raise IOError(f"Unable to access document at {file_url}") from exc

    # 2. Retrieve the expected signature for this document
    doc_id = _extract_doc_id(file_url)
    expected_sig_hex = DOC_SIGNATURES.get(doc_id)

    if expected_sig_hex is None:
        # No known signature for this document – treat as invalid
        return False

    # 3. Compare the provided signature with the expected one securely.
    try:
        # Convert both signatures to bytes for a safe comparison
        provided_sig = bytes.fromhex(sign)
    except ValueError:
        # Signature not a valid hex string
        return False

    # Use hmac.compare_digest to avoid timing attacks.
    return hmac.compare_digest(provided_sig, expected_sig_hex)