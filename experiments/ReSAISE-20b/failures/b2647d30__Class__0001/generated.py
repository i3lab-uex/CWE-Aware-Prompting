# -*- coding: utf-8 -*-
"""
Document management utility – alteration of documents.
"""

from typing import Dict

# Sample in‑memory database structure
DOCUMENTS_DB: Dict[str, dict] = {
    # Example entry:
    # "doc_123": {"document_id": "doc_123", "owner_id": "user_a", "content": "Old content"},
}

def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    operator_id : str
        ID of the user attempting to modify the document.
    operator_role : str
        Role of the user – must be 'editor' to modify documents.
    doc_id : str
        Unique ID of the target document.
    doc_owner_id : str
        Owner ID that must match the stored owner of the document.
    updated_content : str
        New content to replace the current document text.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    KeyError
        If `doc_id` does not exist in :data:`DOCUMENTS_DB`.
    PermissionError
        If the operator is not authorized to modify the document.
    """
    # 1. Validate existence of the document
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_id}' not found.") from exc

    # 2. Verify that the provided owner ID matches the stored one
    if doc_owner_id != doc.get("owner_id"):
        raise PermissionError(
            f"Owner ID mismatch: expected '{doc.get('owner_id')}', got '{doc_owner_id}'."
        )

    # 3. Authorization check – only editors are allowed to modify
    if operator_role.lower() != "editor":
        raise PermissionError(
            f"User '{operator_id}' with role '{operator_role}' is not authorized to edit documents."
        )

    # 4. Ensure the operator is indeed the owner of the document
    if operator_id != doc.get("owner_id"):
        raise PermissionError(
            f"User '{operator_id}' does not own the document and cannot modify it."
        )

    # 5. Perform the update
    doc["content"] = updated_content

    # 6. Return the new content for confirmation
    return doc["content"]