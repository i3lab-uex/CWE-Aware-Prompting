#!/usr/bin/env python3
"""
Utility to embed user supplied text into an XML template safely.
"""

from xml.sax.saxutils import escape
from typing import Final

# Example XML pattern. Replace with the actual template as needed.
xml_pattern: Final[str] = (
    '<?xml version="1.0" encoding="UTF-8"?><response>'
    '<message>{user_text}</message></response>'
)


def create_xml_reply(user_text: str) -> str:
    """
    Insert user-supplied text into a predefined XML template.

    The function escapes any characters that have special meaning in XML
    (e.g., <, >, &, ', ") to prevent malformed XML or injection attacks.

    Parameters
    ----------
    user_text : str
        The content submitted by the user that will be placed into the XML template.

    Returns
    -------
    str
        The final XML response with user content included at the appropriate position.
    """
    # Escape special XML characters in the user input
    safe_text = escape(user_text, {"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped user text
    return xml_pattern.format(user_text=safe_text)


# Example usage:
if __name__ == "__main__":
    sample_user_input = 'Hello <World> & "Everyone"'
    print(create_xml_reply(sample_user_input))