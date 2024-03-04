"""
macOS convenience functions
"""

import platform
import sys

from vsutillib.process import RunCommand


def isSystemInDarkMode() -> bool:
    """
    Detect Dark Mode
    """

    if platform.system() == "Darwin":
        return isMacDarkMode()

    elif platform.system() == "Linux":
        return isLinuxDarkMode()

    elif (platform.system() == "Windows"):
        return isWindowsDarkMode()

    return False

def isMacDarkMode() -> bool:
    """
    Test for macOS Mojave Dark Mode

    Returns:
        bool:

        True if the macOS is using Dark Mode

        False if not or if called on other operating systems
    """

    if platform.system() == "Darwin":
        cmd = RunCommand("defaults read -g AppleInterfaceStyle")

        if getattr(sys, 'frozen', False):
            # running in pyinstaller bundle dark mode does not apply
            return False

        if cmd.run():
            for e in cmd.output:
                if e.find("Dark") >= 0:
                    return True

    return False

def isLinuxDarkMode() -> bool:
    """
    Test for Linux dark mode tested on ubuntu
    For Linux using the following commands

    $ gsettings get org.gnome.desktop.interface color-scheme
    'prefer-dark'

    $ gsettings get org.gnome.desktop.interface gtk-theme
    'Yaru-dark

    Returns:
        bool:

        True if the macOS is using Dark Mode

        False if not or if called on other operating systems
    """

    if platform.system() == "Linux":

        cmd = RunCommand("gsettings get org.gnome.desktop.interface color-scheme")

        if cmd.run():
            for e in cmd.output:
                if e.upper().find("DARK") >= 0:
                    return True
        else:
            cmd.command = "gsettings get org.gnome.desktop.interface gtk-theme"

            if cmd.run():
                for e in cmd.output:
                    if e.upper().find("DARK") >= 0:
                        return True

    return False

def isWindowsDarkMode() -> bool:

    if (platform.system() == "Windows"):
        from winreg import ConnectRegistry, HKEY_CURRENT_USER, QueryValueEx, OpenKey

        aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
        appsUseLightTheme = ""

        try:
            aKey = OpenKey(aReg, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
            appsUseLightTheme = QueryValueEx(aKey, "AppsUseLightTheme")

        except FileNotFoundError:
            return False

        # appsUseLightTheme[0] is 1 when is Light mode 0 if Dark
        if (appsUseLightTheme[0] == 0):
            return True

    return False
