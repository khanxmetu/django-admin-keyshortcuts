import { install, uninstall } from './vendor/hotkey/hotkey.js';

'use strict';
{
    let shortcutsEnabled = localStorage.getItem('django.admin.shortcutsEnabled') || 'true';

    function installShortcuts() {
        for (const el of document.querySelectorAll('[data-hotkey]')) {
            install(el);
        }
    }
    function uninstallShortcuts() {
        for (const el of document.querySelectorAll('[data-hotkey]')) {
            uninstall(el);
        }
    }

    function initShortcuts() {
        const toggleShortcuts = document.getElementById('toggle-shortcuts');

        if (shortcutsEnabled === 'true') {
            toggleShortcuts.checked = true;
            installShortcuts();
        }
        toggleShortcuts.addEventListener('change', function() {
            if (shortcutsEnabled === 'true') {
                shortcutsEnabled = 'false';
                uninstallShortcuts();
            } else {
                shortcutsEnabled = 'true';
                installShortcuts();
            }
            localStorage.setItem('django.admin.shortcutsEnabled', shortcutsEnabled);
        });
    }


    function showShortcutsDialog() {
        const dialog = document.getElementById("shortcuts-dialog");
        dialog.showModal();
    }

    function showDialogOnClick() {
        const dialogButton = document.getElementById("open-shortcuts");
        if(!dialogButton) {
            return;
        }
        dialogButton.addEventListener("click", showShortcutsDialog);
    }


    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initShortcuts);
        document.addEventListener("DOMContentLoaded", showDialogOnClick);
    } else {
        initShortcuts();
        showDialogOnClick();
    }
}
