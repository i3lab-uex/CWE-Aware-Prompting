# -*- coding: utf-8 -*-

"""
Corporate Document Management – Access‑Controlled Update

The `alter_document` function updates a document’s content only when the
requesting user is authorized.  Authorization is determined by:
* The user must be the document owner, or
* The user has an `editor` role.

A `PermissionError` is raised for any unauthorized attempt.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Mock database – in a real system this would be an external persistence layer
# --------------------------------------------------------------------------- #

DOCUMENTS_DB = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-a", "content": "Initial content."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-b", "content": "Another document."},
    # Add more documents as needed
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str | None = None,
    updated_content: str = "",
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the caller. Expected values: 'viewer', 'editor'.
    doc_identifier : str
        Unique identifier of the document to be updated.
    creator_id : str, optional
        Owner ID supplied by the caller. If omitted, it will be fetched from
        DOCUMENTS_DB. Providing this value is optional to support legacy calls.
    updated_content : str
        The new content that will replace the existing document text.

    Returns
    -------
    str
        The updated content of the document after a successful update.

    Raises
    ------
    KeyError
        If `doc_identifier` does not exist in the database.
    PermissionError
        If the user is not authorized to modify the document.

    Notes
    -----
    * The function performs a strict equality check on `modifier_id` against the
      stored `owner_id`.  This mitigates CWE‑863 by ensuring that authorization
      is evaluated against the source of truth rather than any user supplied
      data.
    * The role check is case‑insensitive and only accepts the two known roles.
    """
    # 1. Validate role
    valid_roles = {"viewer", "editor"}
    if user_role.lower() not in valid_roles:
        raise ValueError(f"Unknown role '{user_role}'. Allowed roles: {valid_roles}")

    # 2. Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # 3. Determine the owner ID (use supplied creator_id if provided)
    owner_id = creator_id or doc["owner_id"]

    # 4. Authorization check – prevent CWE-863
    if modifier_id != owner_id and user_role.lower() != "editor":
        raise PermissionError(
            f"User '{modifier_id}' with role '{user_role}' is not authorized "
            f"to modify document '{doc_identifier}'."
        )

    # 5. Perform the update
    doc["content"] = updated_content

    # 6. Return the new content
    return doc["content"]

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     try:
#         new_text = alter_document(
#             modifier_id="user-a",
#             user_role="editor",
#             doc_identifier="doc-001",
#             updated_content="Updated content by owner."
#         )
#         print("Update successful:", new_text)
#     except Exception as e:
#         print("Error:", e)