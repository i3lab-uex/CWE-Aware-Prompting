import urllib.request
import urllib.error
import hmac

# Global dictionary containing the correct signatures for documents.
# Example: DOC_SIGS = {"https://example.com/doc1.pdf": "abcdef123456"}
DOC_SIGS: dict[str, str] = {}

def check_document(url: str, sign_hash: str) -> bool:
    """
    Verify that a document at *url* is accessible and that its cryptographic
    signature matches the expected value stored in DOC_SIGS.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    sign_hash : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value and the URL is
        reachable, False otherwise.

    Raises
    ------
    IOError
        If the document at *url* cannot be accessed (network error, HTTP
        status >= 400, etc.).
    """
    # Check that the URL is reachable first.
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            # Any 2xx status is considered reachable.
            if resp.status >= 400:
                raise IOError(f"URL {url} returned status code {resp.status}")
    except urllib.error.HTTPError as e:
        raise IOError(f"HTTP error accessing {url}: {e}") from e
    except urllib.error.URLError as e:
        raise IOError(f"URL error accessing {url}: {e}") from e
    except Exception as e:
        raise IOError(f"Unexpected error accessing {url}: {e}") from e

    # Retrieve the expected signature for this URL.
    expected = DOC_SIGS.get(url)
    if expected is None:
        # No known signature for this URL; treat as invalid.
        return False

    # Use constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(sign_hash, expected)