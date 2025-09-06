'use strict';
{
    let rows = null;
    let currentRow = null;

    function setUpShortcuts() {
        rows = Array.from(document.querySelectorAll("#result_list thead tr, #result_list tbody tr"));
        // Let rows receive programmatic focus
        rows.forEach(row => {
            row.setAttribute("tabindex", "-1");
        });
    }

    function focusPreviousRow() {
        if (!rows.length) {
            return;
        }
        if (!currentRow || currentRow === rows[0]) {
            currentRow = rows[rows.length - 1];
        } else {
            currentRow = rows[rows.indexOf(currentRow) - 1];
        }
        currentRow.focus();
    }

    function focusNextRow() {
        if (!rows.length) {
            return;
        }
        if (!currentRow || currentRow === rows[rows.length - 1]) {
            currentRow = rows[0];
        } else {
            currentRow = rows[rows.indexOf(currentRow) + 1];
        }
        currentRow.focus();
    }

    function selectCheckbox() {
        if (currentRow) {
            const currentCheckbox = currentRow.querySelector("#action-toggle, .action-select");
            currentCheckbox.click();
        }
    }

    function isHeaderRow(row) {
        return row.parentElement.tagName === "THEAD";
    }

    function openFocusedRow() {
        if (currentRow && !isHeaderRow(currentRow)) {
            const firstLink = currentRow.querySelector("th a");
            if (firstLink) {
                window.location.href = firstLink.href;
            }
        }
    }

    function selectActionsSelect() {
        const actionsSelect = document.querySelector("select[name=action]");
        actionsSelect.focus();
    }

    function bindShortcutActionsToButtons() {
        document.getElementById("keyshortcut-prev-btn").addEventListener("click", focusPreviousRow);
        document.getElementById("keyshortcut-next-btn").addEventListener("click", focusNextRow);
        document.getElementById("keyshortcut-select-btn").addEventListener("click", selectCheckbox);
        document.getElementById("keyshortcut-open-btn").addEventListener("click", openFocusedRow);
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

