import platform
from contextlib import contextmanager

from django.contrib.admin.tests import AdminSeleniumTestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Language
from .models import Paper


class GlobalShortcuts:
    SHOW_DIALOG = "Shift+?"
    CLOSE_DIALOG = "Escape"
    GO_TO_INDEX = "g i"
    TOGGLE_SIDEBAR = "["


class ChangeListShortcuts:
    FOCUS_PREV_ROW = "k"
    FOCUS_NEXT_ROW = "j"
    TOGGLE_ROW_SELECTION = "x"
    FOCUS_ACTIONS_DROPDOWN = "a"
    FOCUS_SEARCH = "/"


class ChangeFormShortcuts:
    SAVE = "Mod+s"
    SAVE_AND_ADD_ANOTHER = "Mod+Shift+S"
    SAVE_AND_CONTINUE = "Mod+Alt+s"
    DELETE = "Alt+d"


class DeleteConfirmationShortcuts:
    CONFIRM_DELETE = "Alt+y"
    CANCEL_DELETE = "Alt+n"


class AdminKeyboardShorcutsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="super",
            password="secret",
            email="super@example.com",
        )

    def setUp(self):
        self.client.force_login(self.superuser)

    def test_shortcuts_dialog_on_index(self):
        response = self.client.get(reverse("test_admin_keyboard_shortcuts:index"))
        self.assertContains(
            response,
            f'<button id="open-shortcuts" data-hotkey="{GlobalShortcuts.SHOW_DIALOG}">',
        )
        self.assertContains(
            response, '<dialog class="keyboard-shortcuts" id="shortcuts-dialog">'
        )
        self.assertContains(response, '<input type="checkbox" id="toggle-shortcuts">')

    def test_shortcuts_dialog_not_on_login(self):
        self.client.logout()
        response = self.client.get(reverse("test_admin_keyboard_shortcuts:login"))
        self.assertNotContains(
            response,
            f'<button id="open-shortcuts" data-hotkey="{GlobalShortcuts.SHOW_DIALOG}">',
        )
        self.assertNotContains(
            response, '<dialog class="keyboard-shortcuts" id="shortcuts-dialog">'
        )
        self.assertNotContains(
            response, '<script src="/static/admin/js/shortcuts.js"></script>'
        )

    def test_shortcuts_dialog_descriptions(self):
        response = self.client.get(reverse("test_admin_keyboard_shortcuts:index"))

        self.assertEqual(GlobalShortcuts.SHOW_DIALOG, "Shift+?")
        self.assertContains(
            response,
            '<dt class="shortcut-description">Show this dialog</dt>'
            '<dd class="shortcut-keys"><kbd>Shift</kbd>+<kbd>?</kbd></dd>',
            html=True,
        )

    def test_shortcuts_dialog_descriptions_for_mac(self):
        self.client.defaults["HTTP_USER_AGENT"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        )
        response = self.client.get(
            reverse("test_admin_keyboard_shortcuts:tests_paper_add")
        )

        self.assertEqual(ChangeFormShortcuts.SAVE, "Mod+s")
        self.assertContains(response, "<kbd>⌘</kbd>+<kbd>s</kbd>")


class SeleniumTests(AdminSeleniumTestCase):
    available_apps = None

    @contextmanager
    def shortcuts_dialog_opened(self):
        """Temporarily opens the shortcuts dialog
        for interacting with elements within dialog
        """
        from selenium.webdriver.common.by import By

        dialog = self.selenium.find_element(By.ID, "shortcuts-dialog")
        open_btn = self.selenium.find_element(By.ID, "open-shortcuts")
        close_btn = dialog.find_element(By.XPATH, ".//button[@aria-label='Close']")

        open_btn.click()
        yield
        close_btn.click()

    def perform_shortcut(self, shortcut):
        """Perform the keyboard shortcut using Selenium."""
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys

        is_mac = platform.system() == "Darwin"

        # split the shortcut keys string into list of list of keys
        # e.g. "Ctrl+S Alt+Shift+X" -> [["Ctrl", "S"], ["Alt", "Shift", "X"]]
        key_combos = [key_combo.split("+") for key_combo in shortcut.split(" ")]

        # parse modifiers
        special_keys = {
            "ctrl": Keys.CONTROL,
            "alt": Keys.ALT,
            "shift": Keys.SHIFT,
            "escape": Keys.ESCAPE,
            "mod": Keys.META if is_mac else Keys.CONTROL,
        }
        key_combos = [
            [special_keys.get(key.lower(), key) for key in combo]
            for combo in key_combos
        ]

        # Temporary workaround to remove focus from textarea/input fields.
        # Currently, Github hotkey prevents shortcuts
        # from triggering when focused on textareas.
        self.selenium.execute_script("document.activeElement.blur();")

        # perform the key combinations
        actions = ActionChains(self.selenium)
        for combo in key_combos:
            for key in combo:
                actions.key_down(key)
            for key in combo:
                actions.key_up(key)
        actions.perform()

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="super",
            password="secret",
            email="super@example.com",
        )
        self.admin_login(
            username="super",
            password="secret",
            login_url=reverse("test_admin_keyboard_shortcuts:index"),
        )

    def test_shortcuts_toggle_on_by_default(self):
        from selenium.webdriver.common.by import By

        self.selenium.execute_script(
            "localStorage.removeItem('django.admin.shortcutsEnabled')"
        )
        self.selenium.refresh()
        toggle = self.selenium.find_element(By.ID, "toggle-shortcuts")
        self.assertTrue(toggle.is_selected())

    def test_shortcuts_toggle_state_persists(self):
        from selenium.webdriver.common.by import By

        # Start with toggle off state
        toggle = self.selenium.find_element(By.ID, "toggle-shortcuts")
        if toggle.is_selected():
            with self.shortcuts_dialog_opened():
                toggle.click()

        # Enable shortcuts
        with self.shortcuts_dialog_opened():
            toggle.click()
        self.assertTrue(toggle.is_selected())
        self.assertEqual(
            self.selenium.execute_script(
                "return localStorage.getItem('django.admin.shortcutsEnabled')"
            ),
            "true",
        )

        # Check state persists after refresh
        self.selenium.refresh()
        toggle = self.selenium.find_element(By.ID, "toggle-shortcuts")
        self.assertTrue(toggle.is_selected())

        # Disable shortcuts
        with self.shortcuts_dialog_opened():
            toggle.click()
        self.assertFalse(toggle.is_selected())
        self.assertEqual(
            self.selenium.execute_script(
                "return localStorage.getItem('django.admin.shortcutsEnabled')"
            ),
            "false",
        )

        # Check state persists after refresh
        self.selenium.refresh()
        toggle = self.selenium.find_element(By.ID, "toggle-shortcuts")
        self.assertFalse(toggle.is_selected())

    def test_shortcuts_disabled_when_toggle_off(self):
        from selenium.webdriver.common.by import By

        toggle = self.selenium.find_element(By.ID, "toggle-shortcuts")

        # Toggle off
        if toggle.is_selected():
            with self.shortcuts_dialog_opened():
                toggle.click()

        # "?" shortcut key does not open the shortcuts dialog
        self.perform_shortcut(GlobalShortcuts.SHOW_DIALOG)
        self.assertFalse(
            self.selenium.find_element(By.ID, "shortcuts-dialog").is_displayed()
        )

    def test_shortcut_global_open_shortcuts_dialog(self):
        from selenium.webdriver.common.by import By

        dialog = self.selenium.find_element(By.ID, "shortcuts-dialog")

        self.perform_shortcut(GlobalShortcuts.SHOW_DIALOG)
        self.assertTrue(dialog.is_displayed())
        self.perform_shortcut(GlobalShortcuts.CLOSE_DIALOG)
        self.assertFalse(dialog.is_displayed())

    def test_shortcut_global_go_to_index(self):
        # Url other than admin index to start with
        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_language_changelist")
        )
        with self.wait_page_loaded():
            self.perform_shortcut(GlobalShortcuts.GO_TO_INDEX)
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url + reverse("test_admin_keyboard_shortcuts:index"),
        )

    def test_shortcut_global_toggle_sidebar(self):
        from selenium.webdriver.common.by import By

        l1 = Language.objects.create(iso="l1")

        pages = [
            reverse("test_admin_keyboard_shortcuts:tests_language_changelist"),
            reverse("test_admin_keyboard_shortcuts:tests_language_add"),
            reverse(
                "test_admin_keyboard_shortcuts:tests_language_delete", args=(l1.pk,)
            ),
        ]
        for page in pages:
            self.selenium.get(self.live_server_url + page)
            sidebar = self.selenium.find_element(By.ID, "nav-sidebar")

            visibility = sidebar.is_displayed()
            self.perform_shortcut(GlobalShortcuts.TOGGLE_SIDEBAR)
            self.assertEqual(sidebar.is_displayed(), not visibility)

            visibility = sidebar.is_displayed()
            self.perform_shortcut(GlobalShortcuts.TOGGLE_SIDEBAR)
            self.assertEqual(sidebar.is_displayed(), not visibility)

    def test_shortcut_changelist_focus_next_row(self):
        from selenium.webdriver.common.by import By

        Language.objects.create(iso="l1")
        Language.objects.create(iso="l2")

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_language_changelist")
        )

        action_toggle_checkbox = self.selenium.find_element(By.ID, "action-toggle")
        l1_checkbox = self.selenium.find_element(
            By.CSS_SELECTOR, "input[name='_selected_action'][value='l1']"
        )
        l2_checkbox = self.selenium.find_element(
            By.CSS_SELECTOR, "input[name='_selected_action'][value='l2']"
        )

        # On first trigger, "focus next row" shortcut
        # focuses Select all objects checkbox
        self.perform_shortcut(ChangeListShortcuts.FOCUS_NEXT_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, action_toggle_checkbox)

        self.perform_shortcut(ChangeListShortcuts.FOCUS_NEXT_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, l1_checkbox)

        self.perform_shortcut(ChangeListShortcuts.FOCUS_NEXT_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, l2_checkbox)

        # Rolls over from last row/checkbox to the first row/checkbox
        self.perform_shortcut(ChangeListShortcuts.FOCUS_NEXT_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, action_toggle_checkbox)

    def test_shortcut_changelist_focus_previous_row(self):
        from selenium.webdriver.common.by import By

        Language.objects.create(iso="l1")
        Language.objects.create(iso="l2")

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_language_changelist")
        )

        l1_checkbox = self.selenium.find_element(
            By.CSS_SELECTOR, "input[name='_selected_action'][value='l1']"
        )
        l2_checkbox = self.selenium.find_element(
            By.CSS_SELECTOR, "input[name='_selected_action'][value='l2']"
        )

        # On first trigger, "focus previous row" shortcut focuses last row/checkbox
        self.perform_shortcut(ChangeListShortcuts.FOCUS_PREV_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, l2_checkbox)

        self.perform_shortcut(ChangeListShortcuts.FOCUS_PREV_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, l1_checkbox)

    def test_shortcut_changelist_toggle_row_selection(self):
        from selenium.webdriver.common.by import By

        Language.objects.create(iso="l1")
        Language.objects.create(iso="l2")

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_language_changelist")
        )

        action_toggle_checkbox = self.selenium.find_element(By.ID, "action-toggle")
        l1_checkbox = self.selenium.find_element(
            By.CSS_SELECTOR, "input[name='_selected_action'][value='l1']"
        )
        l2_checkbox = self.selenium.find_element(
            By.CSS_SELECTOR, "input[name='_selected_action'][value='l2']"
        )

        # Mark l2
        self.perform_shortcut(ChangeListShortcuts.FOCUS_PREV_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, l2_checkbox)

        self.perform_shortcut(ChangeListShortcuts.TOGGLE_ROW_SELECTION)
        self.assertTrue(l2_checkbox.is_selected())

        # Unmark l2
        self.perform_shortcut(ChangeListShortcuts.TOGGLE_ROW_SELECTION)
        self.assertFalse(l2_checkbox.is_selected())

        # Mark action toggle checkbox
        self.perform_shortcut(ChangeListShortcuts.FOCUS_PREV_ROW)
        self.perform_shortcut(ChangeListShortcuts.FOCUS_PREV_ROW)
        self.assertEqual(self.selenium.switch_to.active_element, action_toggle_checkbox)

        self.perform_shortcut(ChangeListShortcuts.TOGGLE_ROW_SELECTION)
        self.assertTrue(action_toggle_checkbox.is_selected())
        self.assertTrue(l1_checkbox.is_selected())
        self.assertTrue(l2_checkbox.is_selected())

    def test_shortcut_changelist_focus_actions_dropdown(self):
        from selenium.webdriver.common.by import By

        Language.objects.create(iso="l1")

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_language_changelist")
        )

        actions_dropdown = self.selenium.find_element(
            By.CSS_SELECTOR, "select[name='action']"
        )

        self.perform_shortcut(ChangeListShortcuts.FOCUS_ACTIONS_DROPDOWN)
        self.assertEqual(self.selenium.switch_to.active_element, actions_dropdown)

    def test_shortcut_changelist_focus_search(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_language_changelist")
        )

        searchbar = self.selenium.find_element(By.ID, "searchbar")
        self.perform_shortcut(ChangeListShortcuts.FOCUS_SEARCH)
        self.assertEqual(self.selenium.switch_to.active_element, searchbar)

    def test_shortcut_changeform_save(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_paper_add")
        )

        title_input = self.selenium.find_element(By.ID, "id_title")
        title_input.send_keys("p1")

        with self.wait_page_loaded():
            self.perform_shortcut(ChangeFormShortcuts.SAVE)
        self.assertEqual(Paper.objects.count(), 1)
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_paper_changelist"),
        )

    def test_shortcut_changeform_save_and_add_another(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_paper_add")
        )

        title_input = self.selenium.find_element(By.ID, "id_title")
        title_input.send_keys("p1")

        with self.wait_page_loaded():
            self.perform_shortcut(ChangeFormShortcuts.SAVE_AND_ADD_ANOTHER)
        self.assertEqual(Paper.objects.count(), 1)
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_paper_add"),
        )

    def test_shortcut_changeform_save_and_continue_editing(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url
            + reverse("test_admin_keyboard_shortcuts:tests_paper_add")
        )

        title_input = self.selenium.find_element(By.ID, "id_title")
        title_input.send_keys("t1")

        with self.wait_page_loaded():
            self.perform_shortcut(ChangeFormShortcuts.SAVE_AND_CONTINUE)
        self.assertEqual(Paper.objects.count(), 1)

        # check if on changeform page for that same saved object
        paper = Paper.objects.first()
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url
            + reverse(
                "test_admin_keyboard_shortcuts:tests_paper_change",
                args=(paper.pk,),
            ),
        )

    def test_shortcut_changeform_delete(self):
        paper = Paper.objects.create(title="p1")
        self.selenium.get(
            self.live_server_url
            + reverse(
                "test_admin_keyboard_shortcuts:tests_paper_change",
                args=(paper.pk,),
            )
        )

        with self.wait_page_loaded():
            self.perform_shortcut(ChangeFormShortcuts.DELETE)
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url
            + reverse(
                "test_admin_keyboard_shortcuts:tests_paper_delete",
                args=(paper.pk,),
            ),
        )

        # Cancel delete
        with self.wait_page_loaded():
            self.perform_shortcut(DeleteConfirmationShortcuts.CANCEL_DELETE)
        self.assertEqual(Paper.objects.count(), 1)
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url
            + reverse(
                "test_admin_keyboard_shortcuts:tests_paper_change",
                args=(paper.pk,),
            ),
        )

        with self.wait_page_loaded():
            self.perform_shortcut(ChangeFormShortcuts.DELETE)
        # Confirm delete
        with self.wait_page_loaded():
            self.perform_shortcut(DeleteConfirmationShortcuts.CONFIRM_DELETE)
        self.assertEqual(Paper.objects.count(), 0)
