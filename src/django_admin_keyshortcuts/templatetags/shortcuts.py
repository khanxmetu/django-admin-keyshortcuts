import re

from django import template
from django.utils.html import format_html_join
from django.utils.translation import gettext as _

register = template.Library()


@register.simple_tag
def get_shortcuts():
    return {
        "global": {
            "show_dialog": (_("Show this dialog"), "Shift+?"),
            "go_to_index": (_("Go to the site index"), "g i"),
        },
        "changelist": {
            "focus_prev_row": (_("Focus previous row"), "k"),
            "focus_next_row": (_("Focus next row"), "j"),
            "toggle_row_selection": (_("Toggle row selection"), "x"),
            "focus_actions_dropdown": (_("Focus actions dropdown"), "a"),
        },
        "changeform": {
            "save": (_("Save"), "Mod+s"),
            "save_and_add_another": (_("Save and add another"), "Mod+Shift+S"),
            "save_and_continue": (_("Save and continue editing"), "Mod+Alt+s"),
            "delete": (_("Delete"), "Alt+d"),
        },
        "delete_confirmation": {
            "confirm_delete": (_("Confirm deletion"), "Alt+y"),
            "cancel_delete": (_("Cancel deletion"), "Alt+n"),
        },
    }


@register.simple_tag(takes_context=True)
def shortcut_format_kbd(context, keyshortcut):
    """Render keyshortcuts like 'Ctrl+S Alt+Shift+X' into HTML kbd elements."""
    user_agent = context["request"].headers.get("User-Agent", "")
    is_mac = re.search(r"Mac|iPod|iPhone|iPad", user_agent)
    labels = {
        "Alt": "⌥" if is_mac else "Alt",
        "Mod": "⌘" if is_mac else "Ctrl",
        "Ctrl": "^" if is_mac else "Ctrl",
    }

    def render_combo(combo):
        # Split by '+', map labels and wrap each key in <kbd>
        keys = [labels.get(key, key) for key in combo.split("+")]
        return format_html_join("+", "<kbd>{}</kbd>", [(key,) for key in keys])

    # Split by ' ', then render each combo
    return format_html_join(
        " ", "{}", [(render_combo(combo),) for combo in keyshortcut.split()]
    )
