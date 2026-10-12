# -*- coding: utf-8 -*-
"""
Document management helper module.

The `alter_document` function allows authorized users to replace the
content of an existing document.  Only users with the role ``editor``
and who own the document may modify it.  All other attempts raise
``PermissionError`` to avoid CWE‑284: Improper Access Control.
"""

from typing import Dict

# Example in-memory document database
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # doc_id : { 'document_id': ..., 'owner_id': ..., 'content': ... }
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content"},
    # Add more documents as needed
}


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str
) -> str:
    """
    Replace the content of an existing document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting to modify the document.
    operator_role : str
        The role of the user ('viewer' or 'editor').
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        Owner ID recorded in the database for this document.
    updated_content : str
        New content to store.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the operator is not an editor or does not own the document.
    KeyError
        If `doc_id` is not present in ``DOCUMENTS_DB``.
    """

    # Ensure the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with id '{doc_id}' does not exist.")

    # Validate ownership
    if operator_role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role can modify documents.")

    if operator_id != doc_owner_id:
        raise PermissionError("Only the document owner can modify this document.")

    # Perform the update
    DOCUMENTS_DB[doc_id]["content"] = updated_content

    return DOCUMENTS_DB[doc_id]["content"]