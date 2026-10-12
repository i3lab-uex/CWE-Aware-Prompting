import html

# A minimal HTML template containing a placeholder for user supplied content.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Produce a safe HTML string by escaping user supplied content and injecting it
    into a predefined template.

    Parameters
    ----------
    input_content : str
        Raw content supplied by the user that will be inserted into the HTML.

    Returns
    -------
    str
        A complete HTML document with the user content safely escaped to prevent
        cross‑site scripting and other injection attacks.

    Notes
    -----
    * The function uses :func:`html.escape` to neutralize special HTML characters
      (e.g., `<`, `>`, `&`, `"`, `'`).
    * The placeholder `{user_content}` in :data:`HTML_TEMPLATE` is replaced with
      the escaped content.
    * This implementation mitigates CWE‑707 (Improper Neutralization of Structured
      Content) by ensuring the dynamic portion is properly escaped before being
      rendered.
    """
    # Escape user content to avoid injection attacks.
    safe_content = html.escape(input_content, quote=True)

    # Inject the escaped content into the template.
    return HTML_TEMPLATE.format(user_content=safe_content)