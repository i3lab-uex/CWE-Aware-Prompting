import threading

# Mock database of documents.
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content of doc1"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content of doc2"},
}

# A simple thread‑safety lock for database operations.
_db_lock = threading.RLock()


def modify_document(user_id: str, role: str, doc_id: str, doc_owner: str, new_data: str) -> str:
    """
    Update the content of a document if the caller has permission.

    Args:
        user_id: ID of the requesting user.
        role: Role of the user ('viewer' or 'editor').
        doc_id: ID of the document to modify.
        doc_owner: Expected owner ID of the document (redundant but used for double‑check).
        new_data: New content to replace the existing one.

    Returns:
        The updated document content.

    Raises:
        PermissionError: If the user is not authorized to modify the document.
        KeyError: If the document does not exist in DOCUMENTS_DB.
    """
    with _db_lock:
        # Retrieve the document from the database.
        try:
            doc = DOCUMENTS_DB[doc_id]
        except KeyError as exc:
            raise KeyError(f"Document with id '{doc_id}' not found.") from exc

        # Verify that the supplied doc_owner matches the stored owner.
        if doc["owner_id"] != doc_owner:
            raise PermissionError("Document ownership mismatch. Access denied.")

        # Authorization check: only editors or the owner can modify.
        if role != "editor" and user_id != doc["owner_id"]:
            raise PermissionError("You do not have permission to modify this document.")

        # Perform the update.
        doc["content"] = new_data

        # Return the updated content.
        return doc["content"]