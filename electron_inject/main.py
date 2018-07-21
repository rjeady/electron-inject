#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: github.com/tintinweb

import os
import subprocess
import sys
import time
from argparse import ArgumentParser
from connect import ElectronRemoteDebugger
import logging

logger = logging.getLogger(__name__)

def launch_url(url):
    # source: https://stackoverflow.com/questions/4216985/call-to-operating-system-to-open-url
    if sys.platform == 'win32':
        os.startfile(url)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            logger.info('Please open a browser on: ' + url)

def main():
    options = parse_args()
    logging.basicConfig(format='[%(filename)s::%(funcName)s][%(levelname)s] %(message)s',
                        level=logging.WARNING if options.quiet else logging.DEBUG)

    timeout_at = time.time() + int(options.timeout)

    erb = ElectronRemoteDebugger.execute(options.target)

    if options.browser:
        launch_url("http://%(host)s:%(port)s/" % erb.params)

    scripts = determine_scripts_to_run(options)
    inject(erb, timeout_at, scripts)


def parse_args():
    usage = """
    usage:
        electron_inject [options] <electron application>

    example:
        electron_inject --enable-devtools-hotkeys --inject myscript.js /path/to/electron/app [--app-params app-args]
    """
    parser = ArgumentParser(usage=usage)
    parser.add_argument("-q", "--quiet",
                        action="store_true", default=False,
                        help="Don't print debug information [default: %(default)s]")
    parser.add_argument("-d", "--enable-devtools-hotkeys",
                        action="store_true", default=False,
                        help="Enable hotkeys F12 (Toggle Developer Tools) and F5 (Refresh) [default: %(default)s]")
    parser.add_argument("-b", "--browser",
                        action="store_true", default=False,
                        help="Launch Devtools in default browser. [default: %(default)s]")
    parser.add_argument("-t", "--timeout",
                        default=5,
                        help="Try hard to inject for the number of seconds specified [default: %(default)ss]")
    parser.add_argument("-j", "--js",
                        action="append",
                        help="path to JS file to inject")
    parser.add_argument("-c", "--css",
                        action="append",
                        help="path to CSS file to inject")
    parser.add_argument("target",
                        nargs='+',
                        help="Electron app to launch along with its arguments")

    options = parser.parse_args()
    # we will exec the target string directly so wrap quotes around elements with spaces
    options.target = " ".join(map(enquote, options.target)).strip()
    return options

def enquote(str):
    return '"' + str + '"' if " " in str else str


def determine_scripts_to_run(options):
    scripts = []
    if options.enable_devtools_hotkeys:
        scripts.append(read_resource("devtools_hotkeys.js"))
    if options.js is not None:
        for script in options.js:
            scripts.append(open(script, "r").read())
    if options.css is not None:
        for script in options.css:
            scripts.append(create_css_inject_script(open(script, "r").read()))
    return scripts


def read_resource(file_name):
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return open(os.path.join(location, file_name)).read()


def create_css_inject_script(css):
    return read_resource("insert_css.js") + "insert_css(`" + css + "`);"


def inject(erb, timeout, scripts):
    windows_visited = set()
    while True:
        for window in (_ for _ in erb.windows() if _['id'] not in windows_visited):
            try:
                logger.info("injecting scripts into window %s" % window['id'])
                for script in scripts:
                    logger.debug(erb.eval(window, script))
            except Exception as e:
                logger.exception(e)
            finally:
                # patch each window only once
                windows_visited.add(window['id'])

        if time.time() > timeout:
            break
        logger.debug("retrying in 1 second")
        time.sleep(1)


if __name__ == '__main__':
    main()
