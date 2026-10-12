# -*- coding: utf-8 -*-
"""
Document editing helper for a simple in‑memory document management system.

The module exposes a single function `edit_document` that safely updates the
content of an existing document.  It enforces a strict authorization policy:
only users with the role ``'editor'`` are allowed to modify documents, and
the user must either be the document owner or have been granted editor rights.
If these conditions are not met, a ``PermissionError`` is raised.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Sample in‑memory document store.
# Each entry is keyed by a unique ``document_id`` and contains:
#   - document_id: str
#   - owner_id:    str
#   - content:     str
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
    # Additional documents can be added here.
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Update the content of an existing document if the caller is authorized.

    Parameters
    ----------
    member_id : str
        Identifier of the user attempting to edit.
    member_role : str
        Role of the user.  Only ``'editor'`` is permitted to edit documents.
    doc_id : str
        Identifier of the target document in ``DOCUMENTS_DB``.
    doc_owner_id : str
        Owner identifier of the target document.  This is provided to avoid an
        extra lookup; callers must provide accurate data.
    replacement_content : str
        New content that will replace the existing document text.

    Returns
    -------
    str
        The updated content of the document after a successful edit.

    Raises
    ------
    KeyError
        If ``doc_id`` is not present in :data:`DOCUMENTS_DB`.
    PermissionError
        If the caller does not have edit privileges.
    ValueError
        If ``replacement_content`` is empty or None (basic input validation).
    """
    # Basic sanity checks
    if not replacement_content:
        raise ValueError("replacement_content must be a non-empty string")

    # Verify the document exists
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID {doc_id!r} does not exist") from exc

    # Authorization check: role must be 'editor' and the caller must
    # either own the document or have been granted editor rights.
    if member_role.lower() != "editor":
        raise PermissionError(
            f"User {member_id!r} has role '{member_role}', but only editors may modify documents."
        )

    # Ensure the provided owner ID matches the stored one (basic integrity check).
    if doc_owner_id != doc["owner_id"]:
        raise ValueError(
            "Provided owner ID does not match the stored owner for this document."
        )

    # Optionally, check that the member is indeed the owner (strict policy).
    if member_id != doc_owner_id:
        # In a real system, you might check a separate permissions table here.
        raise PermissionError(
            f"User {member_id!r} is not the owner of document {doc_id!r} and cannot edit it."
        )

    # All checks passed; perform the update.
    doc["content"] = replacement_content
    return doc["content"]