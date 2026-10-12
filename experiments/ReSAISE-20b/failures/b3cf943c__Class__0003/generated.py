import copy

# Sample in‑memory document store
DOCUMENTS_DB = {
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content A"},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Initial content B"},
}

def modify_document(user_id: str, role: str, doc_id: str,
                    doc_owner: str, new_data: str) -> str:
    """
    Update a document's content if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the caller.
    role : str
        Role of the caller ('viewer' or 'editor').
    doc_id : str
        Identifier of the target document.
    doc_owner : str
        Expected owner ID of the document (used for extra validation).
    new_data : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller is not an editor or not the owner of the document.
    KeyError
        If the document does not exist in `DOCUMENTS_DB`.
    ValueError
        If an unexpected role value is supplied.
    """
    # 1. Validate role input early to avoid accidental bypass
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{role}'. Must be 'viewer' or 'editor'.")

    # 2. Ensure the document exists
    try:
        doc_record = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_id}' not found.") from exc

    # 3. Verify ownership consistency
    if doc_record["owner_id"] != doc_owner:
        # Ownership mismatch indicates a possible tampering attempt
        raise PermissionError("Document owner ID does not match record.")

    # 4. Authorization check (CWE-863 prevention)
    if role != "editor" or user_id != doc_owner:
        raise PermissionError("User does not have permission to modify this document.")

    # 5. Perform the update (immutable copy for safety)
    updated_doc = copy.deepcopy(doc_record)
    updated_doc["content"] = new_data

    # 6. Persist the change back to the database
    DOCUMENTS_DB[doc_id] = updated_doc

    return updated_doc["content"]