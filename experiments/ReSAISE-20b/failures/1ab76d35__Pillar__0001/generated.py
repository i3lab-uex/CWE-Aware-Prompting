# -*- coding: utf-8 -*-

"""
Utility to generate a safe HTML response by embedding user-provided content
into a predefined template.

The function escapes any special characters in the user content to prevent
Cross‑Site Scripting (XSS) attacks and ensures that the resulting HTML is
well‑formed.

CWE-707 (Improper Neutralization of Structured Data) is mitigated by
using html.escape, which neutralizes HTML special characters before the
content reaches the browser.
"""

import html

# Example template; in real use this would come from your application context
html_template: str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Response</title>
</head>
<body>
    <h1>User Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""


def generate_html_response(user_content: str) -> str:
    """
    Generate an HTML response by safely embedding user-provided content.

    Parameters
    ----------
    user_content : str
        The raw content supplied by the user that will be inserted into the HTML.

    Returns
    -------
    str
        The fully formed, escaped HTML response.
    """
    # Ensure we have a string; if not, convert to empty string
    if user_content is None:
        safe_content = ""
    else:
        # Escape special HTML characters to avoid injection
        safe_content = html.escape(str(user_content), quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)