import threading

# Simulated in‑memory document database
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content"},
    # Add more documents as needed
}

# Lock to protect concurrent updates (simple thread‑safety)
_db_lock = threading.Lock()


def update_document(user_id: str, user_role: str,
                    document_id: str, owner_id: str,
                    new_content: str) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to update.
    user_role : str
        Role of the user ('viewer', 'editor', etc.).
    document_id : str
        ID of the target document.
    owner_id : str
        Expected owner of the document (redundant but used for extra check).
    new_content : str
        New content to write into the document.

    Returns
    -------
    str
        The updated content if authorized.

    Raises
    ------
    ValueError
        If the document does not exist.
    PermissionError
        If the user is not authorized to update the document.
    """
    # Ensure the document exists
    with _db_lock:
        doc = DOCUMENTS_DB.get(document_id)
        if doc is None:
            raise ValueError(f"Document '{document_id}' does not exist")

        # Authorization check: user must be the owner or an editor
        if doc["owner_id"] != owner_id:
            # Owner mismatch – reject to avoid privilege escalation
            raise PermissionError("Owner ID mismatch")

        if user_id != owner_id and user_role.lower() != "editor":
            raise PermissionError("User is not authorized to update this document")

        # Perform the update
        doc["content"] = new_content

    return doc["content"]