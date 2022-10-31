#! /usr/bin/env python3
# -*- coding : utf-8 -*-

"""Customizable converter file, with or without:
- indicator in the system tray
- the main window
- opening the app in the default browser
"""


import os

import flask_fd.gui as fgui
import flask_fd.launchers as fgl

import main_web as flask_app  # use your own names here

# MUST be in your main executable, some paths will be relative to this.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PORT = fgl.free_port()
# =====================================================================


# set the server launcher (here for flask)
def launch_function():
    flask_app.app.run(debug=False, port=PORT)


# create the launcher object
server_launcher = fgl.ServerLauncher(
    port=PORT,
    home_page="/",
    launcher=launch_function)



def open_default(*args):
    """Open the application in the default browser of the system"""
    fgui.open_in_main_browser(port=PORT, home_page="/")


# Building the main interface =========================================

# Browser

# def new_browser(*args):
#     """Creates a browser"""
#     browser = fgui.SillyBrowser(
#         base_dir=BASE_DIR,  # required for correct icon behaviour
#         port=PORT,
#         home_page="/",
#         icon='MD_Imperator_icon',
#         is_main=False,  # closing a main widget closes the entire application
#         )
#     return browser


# Indicator

def new_indicator():
    indicator = fgui.Indicator(
        name="Markdown Imperator",
        base_dir=BASE_DIR,  # required for correct icon behaviour
        icon='MD_Imperator_icon',  # required
        label=None,  # str or None
        menu_items=[
            # ("main window", main_window),
            # ("open application", new_browser),
            ("open Markdown Imperator", open_default),
            "_separator",
        ],
        # closing a main widget closes the entire application and server:
        is_main=True,
        # set the server launcher in a single main widget, only once:
        server_launcher=server_launcher
    )
    indicator.indicator.set_label("Markdown Imperator")
    return indicator


open_default()
new_indicator()
