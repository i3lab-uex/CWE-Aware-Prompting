#!/usr/bin/env python3
"""
Document modification helper.

This module provides a single function `modify_file` that updates the content of
a document in an in‑memory database (`DOCUMENTS_DB`).  The function enforces
access control: only the document owner or a user with an 'editor' role may
modify a file.  All other roles are denied.

The implementation follows CWE‑284 guidelines by explicitly checking the
requester's identity and role before performing any state changes.
"""

from __future__ import annotations

import typing as _t

# Example in‑memory database of documents
DOCUMENTS_DB: dict[str, dict[str, _t.Any]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Hello World"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Python Rocks"},
    # Add more documents as needed
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
        ID of the user attempting the update.
    account_role : str
        Role of the user ('viewer', 'editor', etc.).
    file_id : str
        Identifier of the target document.
    owner_id : str
        Owner ID recorded in the document (for double‑check).
    updated_content : str
        New content to store.

    Returns
    -------
    str
        The updated document content on success.

    Raises
    ------
    ValueError
        If the `file_id` does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the caller is not authorized to modify the document.

    Notes
    -----
    * The function performs a strict equality check on both the `owner_id`
      stored in the document and the provided `owner_id` to guard against
      tampering.
    * The role check is case‑insensitive for convenience.
    """
    # 1. Validate document existence
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    doc = DOCUMENTS_DB[file_id]

    # 2. Verify owner consistency
    if doc.get("owner_id") != owner_id:
        raise PermissionError(
            f"Provided owner ID '{owner_id}' does not match the document's actual owner."
        )

    # 3. Access control: only owner or editor can modify
    allowed_roles = {"editor"}  # set of roles permitted to edit
    is_owner = account_id == owner_id
    is_editor_role = account_role.lower() in allowed_roles

    if not (is_owner or is_editor_role):
        raise PermissionError(
            f"User '{account_id}' with role '{account_role}' is not authorized to modify document '{file_id}'."
        )

    # 4. Perform the update
    doc["content"] = updated_content

    return doc["content"]