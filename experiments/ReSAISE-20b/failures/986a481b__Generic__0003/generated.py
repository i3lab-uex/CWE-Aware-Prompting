import threading

# Mock database: a thread‑safe dictionary of documents.
# Each document has:
#   - 'document_id': unique identifier
#   - 'owner_id'    : creator's user ID
#   - 'content'     : current content string
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
}

# A lock to prevent race conditions when multiple threads modify the DB.
_db_lock = threading.Lock()


def revise_document(owner: str, editor_role: str, doc_ref: str,
                    doc_creator: str, revised_content: str) -> str:
    """
    Update a document's content if the user has sufficient permissions.

    Parameters
    ----------
    owner : str
        The ID of the user attempting the update.
    editor_role : str
        Role of the user, expected to be either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to be updated.
    doc_creator : str
        The user ID that originally created the document.
    revised_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to edit the document.
    KeyError
        If the specified document does not exist in the database.
    """
    # Basic validation of role
    if editor_role not in {"viewer", "editor"}:
        raise ValueError("Invalid editor role. Must be 'viewer' or 'editor'.")

    # Ensure the document exists
    with _db_lock:
        if doc_ref not in DOCUMENTS_DB:
            raise KeyError(f"Document with ID '{doc_ref}' does not exist.")

        doc = DOCUMENTS_DB[doc_ref]

    # Authorization check:
    #   * The owner ID stored in the document must match `doc_creator`.
    #   * The user attempting the update (`owner`) must be the creator.
    #   * Only users with role 'editor' are allowed to modify content.
    if doc["owner_id"] != doc_creator:
        raise PermissionError("Document creator mismatch.")

    if owner != doc_creator:
        raise PermissionError("Only the original document creator may edit this document.")

    if editor_role != "editor":
        raise PermissionError("User does not have editing privileges.")

    # Perform the update atomically
    with _db_lock:
        DOCUMENTS_DB[doc_ref]["content"] = revised_content

    return revised_content