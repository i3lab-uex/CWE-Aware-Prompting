# -*- coding: utf-8 -*-
"""
Implementation of the `revise_document` function for a corporate document
management platform.

The function performs a strict authorization check to ensure that only the
document owner or an editor with the appropriate role may modify a document.
If the caller is not authorized, a `PermissionError` is raised.

Security considerations:
- Uses constant‑time string comparison to mitigate timing attacks.
- Explicitly validates that the document exists before attempting modification.
- Avoids side effects by updating only the `content` field in the in‑memory
  database dictionary.
"""

from __future__ import annotations

import hmac
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Sample in‑memory database. In a real system this would be replaced by an
# actual persistence layer (e.g., SQL, NoSQL, or a file system).
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-alice", "content": "Initial content"},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-bob",   "content": "Another document"},
}


def _secure_compare(a: str, b: str) -> bool:
    """
    Perform a constant‑time comparison of two strings.
    This mitigates timing attacks that could otherwise reveal information
    about the internal state of the system.
    """
    return hmac.compare_digest(a, b)


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    owner : str
        The ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller: either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to modify.
    doc_creator : str
        The ID that should match the stored owner of the document.
    revised_content : str
        New content to replace the existing document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the document.
    KeyError
        If `doc_ref` does not exist in :data:`DOCUMENTS_DB`.
    ValueError
        If `editor_role` is not one of the supported roles.
    """
    # Validate role
    if editor_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role: {editor_role!r}")

    # Ensure the document exists
    try:
        doc = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document {doc_ref!r} not found.") from exc

    # Verify that the provided creator matches the stored owner
    if not _secure_compare(doc_creator, doc["owner_id"]):
        raise PermissionError("Document creator mismatch. Unauthorized access.")

    # Authorization logic:
    # - The owner of the document may edit regardless of role.
    # - An editor role is allowed only if they are the owner.
    authorized = (
        _secure_compare(owner, doc["owner_id"])  # Owner check
        or (_secure_compare(editor_role, "editor") and _secure_compare(owner, doc["owner_id"]))
    )

    if not authorized:
        raise PermissionError("User does not have permission to modify this document.")

    # Perform the update
    doc["content"] = revised_content

    return doc["content"]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# try:
#     new_content = revise_document(
#         owner="user-alice",
#         editor_role="editor",
#         doc_ref="doc-001",
#         doc_creator="user-alice",
#         revised_content="Updated content by Alice."
#     )
#     print("Document updated:", new_content)
# except Exception as e:
#     print(f"Error: {e}")