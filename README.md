# injectron

*injectron* allows you to inject CSS and JS into electron based applications.

It has a built in script for enabling F12 devtools and F5 refresh hotkeys.

It was inspired by and based on [electron-inject](https://github.com/tintinweb/electron-inject).

# Installation

To put an `injectron` binary on your PATH, clone this repository and

    $ pip3 install .

or

    $ python3 setup.py install

# Running without installing

You can just run `python3 injectron.py` instead of installing as `injectron` if you prefer.

# Usage

    injectron [options] <electron application>

For example

    injectron --enable-devtools-hotkeys --js my.js --css my.css /path/to/electron/app [--app-params app-args]

You can specify any number of css and js files. Trailing arguments are forwarded to the electron app.

See `--help` for full details.

# How it works

The script will launch the electron app, specifying a debugging port. Then it will connect to that port and evaluate the specified scripts using the debugger.

It will attempt to do this against every window of the application for several seconds (configurable using a timeout argument). This will include looking for embedded webviews.
