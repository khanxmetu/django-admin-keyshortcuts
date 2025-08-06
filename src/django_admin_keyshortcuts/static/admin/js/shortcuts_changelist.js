'use strict';
{
    let checkboxes = null;
    let currentCheckbox = null;

    function setUpShortcuts() {
        checkboxes = Array.from(
            document.querySelectorAll("#action-toggle, .action-select")
        );
    }

    function focusPreviousCheckbox() {
        if (!checkboxes.length) {
            return;
        }
        if (!currentCheckbox || currentCheckbox === checkboxes[0]) {
            currentCheckbox = checkboxes[checkboxes.length - 1];
        } else {
            currentCheckbox = checkboxes[checkboxes.indexOf(currentCheckbox) - 1];
        }
        currentCheckbox.focus();
    }

    function focusNextCheckbox() {
        if (!checkboxes.length) {
            return;
        }
        if (!currentCheckbox || currentCheckbox === checkboxes[checkboxes.length - 1]) {
            currentCheckbox = checkboxes[0];
        } else {
            currentCheckbox = checkboxes[checkboxes.indexOf(currentCheckbox) + 1];
        }
        currentCheckbox.focus();
    }

    function selectCheckbox() {
        if (currentCheckbox) {
            currentCheckbox.click();
        }
    }

    function selectActionsSelect() {
        const actionsSelect = document.querySelector("select[name=action]");
        actionsSelect.focus();
    }

    function bindShortcutActionsToButtons() {
        document.getElementById("keyshortcut-prev-btn").addEventListener("click", focusPreviousCheckbox);
        document.getElementById("keyshortcut-next-btn").addEventListener("click", focusNextCheckbox);
        document.getElementById("keyshortcut-select-btn").addEventListener("click", selectCheckbox);
        document.getElementById("keyshortcut-select-actions-btn").addEventListener("click", selectActionsSelect);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", setUpShortcuts);
        document.addEventListener("DOMContentLoaded", bindShortcutActionsToButtons);
    } else {
        setUpShortcuts();
        bindShortcutActionsToButtons();
    }
}

