import re

from django import template
from django.utils.html import format_html_join
from django.utils.translation import gettext as _

register = template.Library()


@register.simple_tag
def get_shortcuts():
    """
    Returns a dictionary of keyboard shortcuts for use in the help dialog
    and shortcut handling.
    """
    return {
        "global": {
            "show_dialog": (_("Show this dialog"), "Shift+?"),
            "go_to_index": (_("Go to the site index"), "g i"),
        },
        "changelist": {
            "focus_prev_row": (_("Focus previous row"), "k"),
            "focus_next_row": (_("Focus next row"), "j"),
            "toggle_row_selection": (_("Toggle row selection"), "x"),
            "open_focused_row": (_("Open focused row"), "Enter"),
            "focus_actions_dropdown": (_("Focus actions dropdown"), "a"),
            "focus_search": (_("Focus search field"), "/"),
            "toggle_sidebar": (_("Toggle sidebar"), "["),
        },
        "changeform": {
            "save": (_("Save"), "Mod+s"),
            "save_and_add_another": (_("Save and add another"), "Mod+Shift+S"),
            "save_and_continue": (_("Save and continue editing"), "Mod+Alt+s"),
            "delete": (_("Delete"), "Alt+d"),
            "toggle_sidebar": (_("Toggle sidebar"), "["),
        },
        "delete_confirmation": {
            "confirm_delete": (_("Confirm deletion"), "Alt+y"),
            "cancel_delete": (_("Cancel deletion"), "Alt+n"),
            "toggle_sidebar": (_("Toggle sidebar"), "["),
        },
    }


@register.simple_tag(takes_context=True)
def shortcut_format_kbd(context, keyshortcut):
    """Transforms keyshortcut string into HTML kbd elements
    with proper key labels.

    "Mod+S" becomes "<kbd>Ctrl</kbd>+<kbd>S</kbd>" on Windows/Linux
    and "<kbd>⌘</kbd>+<kbd>S</kbd>" on macOS.

    "g i" becomes "<kbd>g</kbd> <kbd>i</kbd>"
    """

    def get_modifier_key_labels_from_request(request):
        """Get modifier key labels based on the user's OS."""
        user_agent = request.headers.get("User-Agent", "")
        is_mac = re.search(r"Mac|iPod|iPhone|iPad", user_agent)

        labels = {
            "Alt": "⌥" if is_mac else "Alt",
            "Mod": "⌘" if is_mac else "Ctrl",
            "Ctrl": "^" if is_mac else "Ctrl",
        }
        return labels

    def render_combo(combo, modifier_labels):
        """Split combo string by "+", map modifier labels and wrap each key in <kbd>."""
        keys = [modifier_labels.get(key, key) for key in combo.split("+")]
        return format_html_join("+", "<kbd>{}</kbd>", [(key,) for key in keys])

    modifier_labels = get_modifier_key_labels_from_request(context["request"])

    # Split the shortcut sequence by " ", then render each shortcut combo
    return format_html_join(
        " ",
        "{}",
        [(render_combo(combo, modifier_labels),) for combo in keyshortcut.split()],
    )
