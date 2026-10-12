# -*- coding: utf-8 -*-
"""
Document management utilities – alter_document implementation.

This module contains a single function, `alter_document`, which allows an
authorized operator to replace the content of an existing document in the
in-memory `DOCUMENTS_DB`.  The function is intentionally simple but
demonstrates proper authorization checks, error handling and defensive
programming against common pitfalls such as incorrect authorization
(CWE‑863).
"""

from __future__ import annotations

import typing as _t

# --------------------------------------------------------------------------- #
# In‑memory document store – for demonstration purposes.
#
# Each entry in DOCUMENTS_DB is a dictionary with the keys:
#   - document_id : str
#   - owner_id    : str
#   - content     : str
#
# The database is deliberately mutable to simulate a real persistence layer.
DOCUMENTS_DB: dict[str, dict[str, _t.Any]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content A."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Initial content B."},
}

# --------------------------------------------------------------------------- #
# Exceptions
class DocumentNotFoundError(KeyError):
    """Raised when the requested document does not exist in DOCUMENTS_DB."""
    pass

# --------------------------------------------------------------------------- #
def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,  # Note: this parameter is redundant but kept for API compatibility
    updated_content: str,
) -> str:
    """
    Replace the content of an existing document.

    Parameters
    ----------
    operator_id : str
        Identifier of the user attempting to modify the document.
    operator_role : str
        Role of the user – must be 'editor' to modify documents.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        Identifier of the document owner (redundant – used only for API compatibility).
    updated_content : str
        New content to replace the current document text.

    Returns
    -------
    str
        The new content of the document after modification.

    Raises
    ------
    PermissionError
        If the operator does not have sufficient privileges.
    DocumentNotFoundError
        If no document with ``doc_id`` exists in the database.

    Notes
    -----
    * Authorization is performed strictly based on ``operator_role``.
      The function does **not** rely on the supplied ``doc_owner_id``
      to make security decisions, thereby avoiding CWE‑863
      (incorrect authorization).  The check ensures that only users with the
      'editor' role can modify any document.
    * The function also validates that ``doc_id`` exists in the database
      before attempting any modification.
    """
    # 1. Verify that the document exists.
    try:
        doc_record = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise DocumentNotFoundError(f"Document with ID '{doc_id}' not found.") from exc

    # 2. Authorization check – only editors are allowed to modify documents.
    if operator_role.lower() != "editor":
        raise PermissionError(
            f"User '{operator_id}' with role '{operator_role}' is not authorized "
            "to modify documents."
        )

    # 3. Update the document content.
    doc_record["content"] = updated_content

    # 4. Return the new content for confirmation.
    return doc_record["content"]


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple test harness – not a full unit test suite.
    import pprint

    print("Before modification:")
    pprint.pprint(DOCUMENTS_DB["doc-001"])

    try:
        new_content = alter_document(
            operator_id="user-789",
            operator_role="editor",
            doc_id="doc-001",
            doc_owner_id="user-123",  # redundant, but kept for API compatibility
            updated_content="Updated content A.",
        )
        print("\nModification successful. New content:")
        print(new_content)
    except Exception as e:
        print(f"\nError: {e}")

    print("\nAfter modification:")
    pprint.pprint(DOCUMENTS_DB["doc-001"])