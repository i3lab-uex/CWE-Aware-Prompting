from __future__ import annotations

import typing as _t

# Example in-memory database; in a real system this would be replaced by persistent storage.
DOCUMENTS_DB: dict[str, dict[str, _t.Any]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "user001", "content": "Initial content."}
}

def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str
) -> str:
    """
    Update the content of a document if the user has sufficient permissions.

    Parameters
    ----------
    modifier_id : str
        ID of the user attempting to modify the document.
    user_role : str
        Role of the user, expected values are 'viewer' or 'editor'.
    doc_identifier : str
        Unique ID of the target document.
    creator_id : str
        Owner ID stored in the database for this document.
    updated_content : str
        New content to replace the existing document text.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the document ID is not found in `DOCUMENTS_DB`.
    """
    # Validate role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {user_role!r}. Expected 'viewer' or 'editor'.")

    # Ensure document exists
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' does not exist.")

    # Authorization check: only editors or the owner can modify
    if user_role != "editor" and modifier_id != creator_id:
        raise PermissionError(
            f"User '{modifier_id}' does not have permission to modify document "
            f"'{doc_identifier}'."
        )

    # Perform the update
    DOCUMENTS_DB[doc_identifier]["content"] = updated_content

    return DOCUMENTS_DB[doc_identifier]["content"]