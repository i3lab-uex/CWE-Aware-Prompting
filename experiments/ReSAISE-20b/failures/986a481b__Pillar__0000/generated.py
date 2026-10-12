# -*- coding: utf-8 -*-

from __future__ import annotations

# Simulated in‑memory document store
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
    # ... additional documents can be added here
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the caller has proper authorization.

    Parameters
    ----------
    owner : str
        The ID of the user attempting the update.
    editor_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_ref : str
        Unique document identifier to modify.
    doc_creator : str
        The creator's user ID for the document (should match DOCUMENTS_DB[doc_ref]['owner_id']).
    revised_content : str
        New content that will replace the existing document text.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified `doc_ref` does not exist in DOCUMENTS_DB.
    ValueError
        If `editor_role` is not one of the expected values.
    """
    # Validate role
    if editor_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {editor_role}")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_ref}' not found.") from exc

    # Check that the supplied creator matches the stored owner
    if doc_creator != doc["owner_id"]:
        raise PermissionError("Provided creator ID does not match document owner.")

    # Authorization check: user must be the owner or have editor role
    if not (owner == doc_creator or editor_role == "editor"):
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    doc["content"] = revised_content

    return doc["content"]