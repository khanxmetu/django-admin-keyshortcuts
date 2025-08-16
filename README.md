# django-admin-keyshortcuts
A Django package that adds keyboard shortcuts to the Django Admin interface for improved accessibility.  

## Demo
A static preview of Django Admin with Keyboard Shortcuts is available at:  
https://khanxmetu.github.io/django-admin-keyshortcuts-demo/

## Setup
Install from pip:  
`pip install django-admin-keyshortcuts`

then add `django_admin_keyshortctus` before `django.contrib.admin` in your `INSTALLED_APPS`:

```
INSTALLED_APPS = (
    ...,
    'django_admin_keyshortcuts',
    'django.contrib.admin', 
    ...,
)
```

## Usage
The following is a list of supported shortcuts
| Description                    | Shortcut (Windows/Linux) | Shortcut (MacOS) | Scope               |
|--------------------------------|--------------------|------------------|---------------------|
| Show shortcuts help dialog     | ?                  | ?                | Global              |
| Go to the site index           | g i                | g i              | Global              |
| Toggle sidebar                 | [                  | [                | Global (where it exists) |
| Select previous row for action | k                  | k                | Change List         |
| Select next row for action     | j                  | j                | Change List         |
| Toggle row selection           | x                  | x                | Change List         |
| Focus actions dropdown         | a                  | a                | Change List         |
| Focus search field             | /                  | /                | Change List         |
| Save and go to change list     | Ctrl+s             | ⌘+s              | Change Form         |
| Save and add another           | Ctrl+Shift+S       | ⌘+Shift+S        | Change Form         |
| Save and continue editing      | Ctrl+Alt+s         | ⌘+⌥+s            | Change Form         |
| Delete                         | Alt+d              | ⌥+d              | Change Form         |
| Confirm deletion               | Alt+y              | ⌥+y              | Delete Confirmation |
| Cancel deletion                | Alt+n              | ⌥+n              | Delete Confirmation |


## About
The **django-admin-keyshortcuts** package is being developed with the goal of eventually merging its functionality into Django core.  
This package has been undergoing refinements with respect to [GSoC 2025: Keyboard Shortcuts Specification](https://docs.google.com/document/d/1sFyl53B4IPWpYX7Q0vJYaNiCaJbe3Ym3_m1Dgk_gmr8/)
