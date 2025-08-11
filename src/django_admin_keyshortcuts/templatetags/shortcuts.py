from django import template
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
            "save": (_("Save"), "Alt+s"),
            "save_and_add_another": (_("Save and add another"), "Alt+a"),
            "save_and_continue": (_("Save and continue editing"), "Alt+c"),
            "delete": (_("Delete"), "Alt+d"),
        },
        "delete_confirmation": {
            "confirm_delete": (_("Confirm deletion"), "Alt+y"),
            "cancel_delete": (_("Cancel deletion"), "Alt+n"),
        },
    }


@register.filter
def shortcut_format_kbd(value):
    combos = value.split()
    return " ".join([f"<kbd>{combo}</kbd>" for combo in combos])
