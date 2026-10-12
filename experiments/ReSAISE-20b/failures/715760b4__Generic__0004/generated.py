# -*- coding: utf-8 -*-

"""
Utility to embed user supplied data into an XML template safely.
"""

from xml.sax.saxutils import escape

# Predefined XML structure containing a placeholder for user content.
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_entry}</message>
</response>"""


def produce_xml_message(user_entry: str) -> str:
    """
    Embed the provided user entry into a predefined XML template.

    The function escapes any characters that could otherwise break
    the XML structure or lead to injection attacks (e.g., "<", ">", "&",
    quotes).

    Parameters
    ----------
    user_entry : str
        The raw string supplied by the user.

    Returns
    -------
    str
        A fully-formed XML document with the user entry safely inserted.
    """
    # Escape special XML characters in the user input
    safe_entry = escape(user_entry, {"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return xml_template.format(user_entry=safe_entry)