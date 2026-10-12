# ──────────────────────────────────────────────────────
# Document revision helper for a corporate platform
# ──────────────────────────────────────────────────────

from __future__ import annotations
from typing import Dict, Any


# Example in‑memory database. In a real system this would be
# replaced by persistent storage (SQL, NoSQL, etc.).
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    "doc_001": {"document_id": "doc_001", "owner_id": "alice", "content": "Initial content"},
    # Add more documents as needed
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the caller has sufficient privileges.

    Parameters
    ----------
    owner : str
        ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller; must be either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to modify.
    doc_creator : str
        The original owner ID stored in the database.
    revised_content : str
        New content that will replace the existing document body.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the caller is not the original owner or an editor.
    KeyError
        If `doc_ref` does not exist in the database.
    ValueError
        If `editor_role` is neither 'viewer' nor 'editor'.
    """

    # Validate the role value
    if editor_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{editor_role}'. Must be 'viewer' or 'editor'.")

    # Ensure the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_ref}' does not exist.")

    # Verify that the caller matches the creator or has editor privileges
    if owner != doc_creator and editor_role != "editor":
        raise PermissionError(
            f"User '{owner}' with role '{editor_role}' is not authorized to modify document '{doc_ref}'."
        )

    # Perform the update
    DOCUMENTS_DB[doc_ref]["content"] = revised_content

    return DOCUMENTS_DB[doc_ref]["content"]