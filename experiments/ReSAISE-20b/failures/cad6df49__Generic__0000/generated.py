# -*- coding: utf-8 -*-
"""
Utility module for constructing an XML reply safely.

The `build_xml_reply` function inserts user-provided text into a predefined
XML template while ensuring that any special characters are properly escaped.
This prevents XML injection attacks and ensures well‑formed output.

Author: OpenAI
"""

from xml.sax.saxutils import escape

# Default XML template with a placeholder for user content.
XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_text}</message>
</response>"""


def build_xml_reply(user_text: str) -> str:
    """
    Build an XML response by embedding the given user text into a template.

    Parameters
    ----------
    user_text : str
        The text supplied by the user. It will be escaped to avoid XML injection.

    Returns
    -------
    str
        A fully-formed XML string containing the escaped user text.

    Notes
    -----
    The function uses :func:`xml.sax.saxutils.escape` to convert characters
    like '&', '<', and '>' into their corresponding XML entities.
    This ensures the output remains well‑formed even when the user supplies
    arbitrary content.

    Example
    -------
    >>> build_xml_reply('Hello <world> & "everyone"')
    '<?xml version="1.0" encoding="UTF-8"?><response><message>Hello &lt;world&gt; &amp; "everyone"</message></response>'
    """
    # Escape user input to prevent XML injection
    safe_text = escape(user_text, entities={"\"": "&quot;", "'": "&apos;"})
    return XML_TEMPLATE.format(user_text=safe_text)