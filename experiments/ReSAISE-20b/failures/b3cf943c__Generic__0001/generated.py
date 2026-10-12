# -*- coding: utf-8 -*-

from typing import Dict

# Example in‑memory document store
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content"},
    # add more documents as needed
}


def modify_document(user_id: str, role: str, doc_id: str, doc_owner: str, new_data: str) -> str:
    """
    Update the content of a document if the caller has proper permissions.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting the update.
    role : str
        Role of the user, expected to be either 'viewer' or 'editor'.
    doc_id : str
        Identifier of the document to modify.
    doc_owner : str
        Expected owner ID for the document (should match DOCUMENTS_DB[doc_id]['owner_id']).
    new_data : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If `doc_id` is not present in DOCUMENTS_DB.
    ValueError
        If the provided `role` is not recognized or if the provided `doc_owner`
        does not match the owner stored in DOCUMENTS_DB.
    """
    # Validate role
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {role}")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.") from exc

    # Ensure the provided doc_owner matches the stored owner
    if doc["owner_id"] != doc_owner:
        raise ValueError("Provided document owner does not match stored owner.")

    # Permission check
    if role == "viewer":
        raise PermissionError("Viewers are not allowed to modify documents.")
    if role == "editor" and user_id != doc_owner:
        raise PermissionError("Editors can only modify their own documents.")

    # Update the content
    doc["content"] = new_data

    return doc["content"]