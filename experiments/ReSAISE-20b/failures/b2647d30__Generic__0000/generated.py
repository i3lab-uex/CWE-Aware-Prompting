# -*- coding: utf-8 -*-
"""
A simple in‑memory document management module.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock database – in a real system this would be replaced by persistent storage
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user123", "content": "Initial content A"},
    "doc-002": {"document_id": "doc-002", "owner_id": "user456", "content": "Initial content B"},
}


# --------------------------------------------------------------------------- #
def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting the modification.
    operator_role : str
        Role of the operator, expected to be either ``'viewer'`` or ``'editor'``.
    doc_id : str
        The unique identifier of the target document.
    doc_owner_id : str
        Expected owner ID for the document (used as an extra check).
    updated_content : str
        The new content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the operator is not allowed to modify the document.
    KeyError
        If the specified ``doc_id`` does not exist in the database.
    ValueError
        If ``operator_role`` is neither 'viewer' nor 'editor'.
    """
    # Validate role
    if operator_role not in {"viewer", "editor"}:
        raise ValueError(f"Unknown role '{operator_role}'. Expected 'viewer' or 'editor'.")

    # Retrieve document – raise KeyError if missing
    doc = DOCUMENTS_DB[doc_id]

    # Verify that the owner matches the stored record
    if doc["owner_id"] != doc_owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # Permission check: only editors may modify, and they must be the owner
    if operator_role != "editor" or operator_id != doc_owner_id:
        raise PermissionError("Insufficient permissions to modify the document.")

    # Perform update (deep copy for safety)
    new_doc = copy.deepcopy(doc)
    new_doc["content"] = updated_content

    # Persist the change back to the mock DB
    DOCUMENTS_DB[doc_id] = new_doc

    return new_doc["content"]


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage – these lines can be removed in production
    try:
        print("Before update:", DOCUMENTS_DB["doc-001"]["content"])
        new_text = alter_document(
            operator_id="user123",
            operator_role="editor",
            doc_id="doc-001",
            doc_owner_id="user123",
            updated_content="Updated content for doc-001",
        )
        print("After update:", new_text)
    except Exception as exc:
        print(f"Error: {exc}")