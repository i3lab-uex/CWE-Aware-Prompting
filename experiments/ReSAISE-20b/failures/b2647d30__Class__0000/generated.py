#!/usr/bin/env python3
"""
A minimal document management helper that safely updates a document.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample in‑memory database
# --------------------------------------------------------------------------- #

DOCUMENTS_DB = {
    "doc001": {"document_id": "doc001", "owner_id": "user123", "content": "Initial content"},
    "doc002": {"document_id": "doc002", "owner_id": "user456", "content": "Another document"},
    # ... add more documents as needed
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of an existing document if the operator is authorized.

    Parameters
    ----------
    operator_id : str
        ID of the user attempting to modify the document.
    operator_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        The owner ID that should match the database entry for the document.
    updated_content : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the operator does not have permission to modify the document.
    KeyError
        If the specified document ID is not found in ``DOCUMENTS_DB``.
    ValueError
        If an unsupported role is provided.
    """

    # --------------------------------------------------------------------- #
    # 1. Validate input parameters
    # --------------------------------------------------------------------- #

    if operator_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role: {operator_role!r}")

    # --------------------------------------------------------------------- #
    # 2. Retrieve the document
    # --------------------------------------------------------------------- #

    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID {doc_id!r} not found") from exc

    # --------------------------------------------------------------------- #
    # 3. Verify the document's owner matches the provided doc_owner_id
    # --------------------------------------------------------------------- #

    if doc["owner_id"] != doc_owner_id:
        raise PermissionError(
            "Provided owner ID does not match the document's actual owner."
        )

    # --------------------------------------------------------------------- #
    # 4. Authorization check (CWE‑863 compliance)
    # --------------------------------------------------------------------- #

    if operator_role == "viewer":
        raise PermissionError("Viewers are not allowed to modify documents.")

    # Editors can edit if they are the owner or any editor (business rule)
    if operator_role == "editor" and operator_id != doc_owner_id:
        # If the system requires that only owners edit, uncomment the next line.
        # raise PermissionError("Only the document owner can modify this document.")
        pass  # allow editors to edit any document in this simplified example

    # --------------------------------------------------------------------- #
    # 5. Perform the update
    # --------------------------------------------------------------------- #

    doc["content"] = updated_content

    # Return the new content for confirmation
    return doc["content"]


# --------------------------------------------------------------------------- #
# Example usage (for testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        new_text = alter_document(
            operator_id="user123",
            operator_role="editor",
            doc_id="doc001",
            doc_owner_id="user123",
            updated_content="Updated content by owner.",
        )
        print("Document successfully updated:", new_text)
    except Exception as e:
        print(f"Error: {e}")