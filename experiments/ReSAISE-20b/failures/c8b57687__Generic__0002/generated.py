# -*- coding: utf-8 -*-

"""
Utility to embed user-provided content safely into an XML template.
"""

from xml.sax.saxutils import escape


def create_xml_output(user_input: str, xml_template: str) -> str:
    """
    Return a fully‑formed XML string with the user input inserted
    into ``xml_template`` at the placeholder {user_input}.

    The function escapes XML special characters in *user_input* to
    prevent injection of malicious markup.

    Parameters:
        user_input (str): Content supplied by the user.
        xml_template (str): XML template containing a single
            placeholder ``{user_input}``.

    Returns:
        str: The XML string with the escaped user content inserted.
    """
    # Escape special XML characters in the user input
    safe_input = escape(user_input, entities={"'": "&apos;", '"': "&quot;"})

    # Insert the escaped content into the template
    return xml_template.format(user_input=safe_input)