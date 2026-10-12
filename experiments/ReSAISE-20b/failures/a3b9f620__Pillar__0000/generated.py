#!/usr/bin/env python3
"""
User profile rendering module.

This module provides a single public function `generate_user_profile`
which sanitizes user supplied data and renders it into an HTML
profile string using a pre‑defined template.  The implementation takes
care to neutralise any HTML special characters to mitigate cross-site
scripting (XSS) attacks and follows the recommendations for
CWE‑707: Improper Neutralisation of Input.

Author: ChatGPT
"""

from __future__ import annotations

import html
import re
from typing import Final

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
# The profile template.  It should contain exactly three placeholders:
# {full_name}, {about_me} and {status_update}.  The placeholders are
# used with the `str.format` method.  Any missing placeholder will raise a
# KeyError which is preferable to silently rendering an incomplete profile.
PROFILE_FORMAT: Final[str] = (
    "<div class=\"user-profile\">\n"
    "  <h2>{full_name}</h2>\n"
    "  <section class=\"about-me\">\n"
    "    <h3>About Me</h3>\n"
    "    <p>{about_me}</p>\n"
    "  </section>\n"
    "  <section class=\"status-update\">\n"
    "    <h3>Status</h3>\n"
    "    <p>{status_update}</p>\n"
    "  </section>\n"
    "</div>"
)

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _sanitize(text: str) -> str:
    """
    Escape special HTML characters in a string to prevent XSS.

    Parameters
    ----------
    text : str
        The raw user input that may contain malicious content.

    Returns
    -------
    str
        A safe string with all `<`, `>`, `&`, `"`, and `'` characters escaped.
    """
    # html.escape already handles &, <, >. We additionally escape quotes
    # to be extra safe when the string is embedded in attributes.
    return html.escape(text, quote=True)


def _ensure_template_well_formed(template: str) -> None:
    """
    Validate that the template contains the required placeholders and no
    stray braces.  This protects against malformed templates which could
    lead to runtime errors or security issues.

    Parameters
    ----------
    template : str
        The profile template string to validate.

    Raises
    ------
    ValueError
        If the template is missing required placeholders or contains
        unmatched braces.
    """
    required_placeholders = {"full_name", "about_me", "status_update"}
    # Find all placeholders in the template
    found = set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", template))
    missing = required_placeholders - found
    if missing:
        raise ValueError(f"Template is missing placeholders: {missing}")

    # Check for unmatched braces (simple heuristic)
    if template.count("{") != template.count("}"):
        raise ValueError("Template contains unmatched braces.")


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Generate a sanitized HTML user profile string.

    Parameters
    ----------
    full_name : str
        The user's self‑provided name.
    about_me : str
        A user‑authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        The fully rendered and sanitized profile ready for web display.

    Raises
    ------
    ValueError
        If the global PROFILE_FORMAT template is malformed.
    """
    # Validate the template once per call.  In a real application this
    # could be cached to avoid repeated work.
    _ensure_template_well_formed(PROFILE_FORMAT)

    # Sanitize each component
    safe_name = _sanitize(full_name)
    safe_about = _sanitize(about_me).replace("\n", "<br>")  # preserve line breaks
    safe_status = _sanitize(status_update)

    # Render the template with sanitized values
    rendered_profile = PROFILE_FORMAT.format(
        full_name=safe_name,
        about_me=safe_about,
        status_update=safe_status,
    )

    return rendered_profile