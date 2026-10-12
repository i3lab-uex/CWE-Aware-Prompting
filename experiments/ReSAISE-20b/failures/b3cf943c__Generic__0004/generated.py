# -*- coding: utf-8 -*-

"""
Document modification module for a corporate document management platform.
"""

from __future__ import annotations

# Sample in‑memory database. In production this would be replaced by
# a persistent datastore (e.g., SQLAlchemy, Django ORM, etc.).
DOCUMENTS_DB: dict[str, dict] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-a", "content": "Initial content."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-b", "content": "Second document."},
    # ... other documents ...
}


def modify_document(
    *,
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str | None = None,
    new_data: str
) -> str:
    """
    Update the content of a document if the user has sufficient permissions.

    Parameters
    ----------
    user_id : str
        Identifier of the requesting user.
    role : str
        Role of the user, expected to be either 'viewer' or 'editor'.
    doc_id : str
        Identifier of the document to be updated.
    doc_owner : str | None, optional
        Cached owner id of the document. If not provided, it will be fetched from
        ``DOCUMENTS_DB``.  Passing the owner explicitly can reduce database look‑ups
        in high‑traffic scenarios.
    new_data : str
        New content that will replace the existing document body.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If ``doc_id`` is not found in ``DOCUMENTS_DB``.
    ValueError
        For invalid role values or empty new_data.

    Notes
    -----
    * Security considerations:
      - The function checks that the user role is either 'viewer' or 'editor'.
      - Only users with role 'editor' and who own the document may modify it.
      - The function does not perform any content sanitisation; callers should
        ensure that ``new_data`` is safe for storage/ display.
    """

    # Validate role
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{role}'. Allowed roles: 'viewer', 'editor'.")

    # Validate new_data
    if not isinstance(new_data, str) or not new_data.strip():
        raise ValueError("new_data must be a non‑empty string.")

    # Retrieve document
    try:
        doc_record = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with id '{doc_id}' not found.") from exc

    # Determine owner (use provided or look up)
    owner_id = doc_owner if doc_owner is not None else doc_record["owner_id"]

    # Authorization logic
    if role == "viewer":
        raise PermissionError("Viewers are not allowed to modify documents.")
    if role == "editor" and user_id != owner_id:
        raise PermissionError("Editors can only modify their own documents.")

    # Perform the update
    doc_record["content"] = new_data

    return doc_record["content"]