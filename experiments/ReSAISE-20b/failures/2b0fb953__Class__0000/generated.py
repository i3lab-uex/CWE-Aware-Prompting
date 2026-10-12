import threading

# Simulated in‑memory document database.
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content"},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document"},
}

# A lock to protect concurrent modifications to the database.
_db_lock = threading.Lock()


def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    account_id : str
        ID of the user making the request.
    account_role : str
        Role of the user (e.g., 'viewer', 'editor').
    file_id : str
        ID of the document to modify.
    owner_id : str
        Expected owner ID of the document (redundant check for safety).
    updated_content : str
        New content to store in the document.

    Returns
    -------
    str
        The updated content on success.
        On unauthorized access, returns an error message.

    Raises
    ------
    ValueError
        If `file_id` is not present in the document database.
    """
    # First, verify that the requested file exists.
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    doc = DOCUMENTS_DB[file_id]

    # Ensure the owner_id matches the stored value (prevents tampering).
    if doc["owner_id"] != owner_id:
        return "Authorization error: Owner ID mismatch."

    # Authorization check: allow if user is the owner or has an 'editor' role.
    authorized = (account_id == doc["owner_id"]) or (account_role.lower() == "editor")

    if not authorized:
        return "Authorization error: User does not have permission to modify this document."

    # Perform the update in a thread‑safe manner.
    with _db_lock:
        doc["content"] = updated_content

    return doc["content"]