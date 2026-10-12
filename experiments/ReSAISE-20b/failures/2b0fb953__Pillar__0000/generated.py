from __future__ import annotations

# Sample in‑memory document database.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Hello World"},
    # Add more documents as needed.
}


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
        Role of the user ('viewer', 'editor', etc.).
    file_id : str
        ID of the document to modify.
    owner_id : str
        Owner (creator) ID of the document. Must match the record in DOCUMENTS_DB.
    updated_content : str
        New content to store.

    Returns
    -------
    str
        The updated document content if the operation succeeded.

    Raises
    ------
    ValueError
        If `file_id` does not exist in the system.
    RuntimeError
        If the caller is not authorized to modify the document.

    Notes
    -----
    * Only users with role 'editor' or who are the document owner may modify a file.
    * The function performs strict equality checks to avoid CWE‑284 (Improper Access Control).
    """
    # 1. Validate that the document exists.
    doc = DOCUMENTS_DB.get(file_id)
    if doc is None:
        raise ValueError(f"Document ID '{file_id}' does not exist.")

    # 2. Validate that the owner_id matches the stored record.
    if doc["owner_id"] != owner_id:
        raise RuntimeError("Provided owner ID does not match the document's actual owner.")

    # 3. Authorization check.
    is_owner = account_id == doc["owner_id"]
    has_editor_privileges = account_role.lower() == "editor"

    if not (is_owner or has_editor_privileges):
        raise RuntimeError("Unauthorized: insufficient permissions to modify the document.")

    # 4. Perform the update.
    doc["content"] = updated_content
    return doc["content"]