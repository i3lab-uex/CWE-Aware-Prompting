import datetime

# Sample in‑memory document store
DOCUMENTS_DB = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-a", "content": "Initial content of doc 1."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-b", "content": "Initial content of doc 2."},
}

def update_document(user_id: str,
                    user_role: str,
                    document_id: str,
                    owner_id: str,
                    new_content: str) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the update.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        ID of the target document.
    owner_id : str
        Expected owner of the document. This is used to double‑check that the
        stored document's `owner_id` matches.
    new_content : str
        The new content to write into the document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    ValueError
        If the requested `document_id` does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorized to modify the document.

    Notes
    -----
    - Only users with role ``'editor'`` or the document owner may update a
      document.
    - The function mutates ``DOCUMENTS_DB`` in place and returns the new
      content for convenience.
    """
    # Validate that the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if doc is None:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # Double‑check that the stored owner matches the provided owner_id
    if doc.get("owner_id") != owner_id:
        raise ValueError(f"Owner ID mismatch for document '{document_id}'.")

    # Authorization check: editor role or owner
    is_owner = (user_id == owner_id)
    is_editor = (user_role.lower() == "editor")
    if not (is_owner or is_editor):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to update document '{document_id}'."
        )

    # Perform the update
    doc["content"] = new_content

    # Optional: add a timestamp for audit purposes (not required by spec)
    doc["last_modified"] = datetime.datetime.utcnow().isoformat() + "Z"

    return doc["content"]