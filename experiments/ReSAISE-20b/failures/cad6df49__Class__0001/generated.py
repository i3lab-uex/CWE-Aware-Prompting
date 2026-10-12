# -*- coding: utf-8 -*-
"""
Utility to safely embed user input into an XML template.
"""

from xml.sax.saxutils import escape


def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Return a fully-formed XML string by inserting the provided user_text
    into the given xml_template. The user input is escaped to prevent XML
    injection (CWE-74).

    Parameters:
        user_text: str
            The text supplied by the user. It will be escaped before being
            inserted into the XML structure.
        xml_template: str
            The XML template containing a single placeholder `{user_text}`.

    Returns:
        str: The XML string with the user text safely embedded.
    """
    # Escape special XML characters in the user supplied content
    safe_text = escape(user_text, entities={"'": "&apos;", '"': "&quot;"})

    # Substitute the placeholder in the template
    return xml_template.format(user_text=safe_text)