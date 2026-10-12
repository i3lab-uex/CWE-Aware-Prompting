# -*- coding: utf-8 -*-
"""
A minimal, secure implementation of a document modification routine for
a corporate-wide document management platform.
"""

from typing import Dict

# Mock database of documents. In a real system this would be replaced
# with calls to a persistent store (e.g., SQL, NoSQL, or an API).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # Example entry:
    # "doc_123": {"document_id": "doc_123", "owner_id": "user_a", "content": "Initial content"}
}


def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the requesting user.
    role : str
        Role of the user ('viewer' or 'editor').  Case-insensitive.
    doc_id : str
        Identifier of the target document.
    doc_owner : str
        Expected owner ID of the document (redundant with database, used for double-check).
    new_data : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If an unsupported role is supplied.
    """
    # ------------------------------------------------------------------
    # 1. Validate input arguments
    # ------------------------------------------------------------------
    if role.lower() not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role: {role!r}")

    # ------------------------------------------------------------------
    # 2. Retrieve the document from the database
    # ------------------------------------------------------------------
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document {doc_id!r} not found") from exc

    # ------------------------------------------------------------------
    # 3. Authorization check (CWE-863 compliance)
    #
    # The check must be performed *after* fetching the resource to avoid
    # race conditions or mis-ordered logic that could lead to incorrect
    # authorizations.  We perform a strict comparison against the stored
    # owner_id and also verify that the supplied doc_owner matches (to
    # guard against stale/incorrect caller data).
    # ------------------------------------------------------------------
    is_owner = doc["owner_id"] == user_id
    owner_matches_provided = doc["owner_id"] == doc_owner

    # Only allow modifications if the user is an editor or the owner
    authorized = (role.lower() == "editor" and is_owner) or is_owner

    if not authorized:
        raise PermissionError(
            f"User {user_id!r} does not have permission to modify document {doc_id!r}"
        )

    if not owner_matches_provided:
        # The supplied doc_owner does not match the database record.
        # This could indicate tampering or a stale client state.
        raise PermissionError(
            f"Document ownership mismatch for {doc_id!r}: "
            f"expected owner {doc['owner_id']!r}, got {doc_owner!r}"
        )

    # ------------------------------------------------------------------
    # 4. Perform the update
    # ------------------------------------------------------------------
    doc["content"] = new_data

    # Optionally, you could persist the change to a real database here.
    # For this mock implementation we simply return the updated content.

    return doc["content"]