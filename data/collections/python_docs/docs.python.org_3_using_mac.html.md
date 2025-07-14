### 5.1.1. Installation steps

For [current Python versions](https://www.python.org/downloads/)
(other than those in `security` status), the release team produces a
**Python for macOS** installer package for each new release.
A list of available installers
is available [here](https://www.python.org/downloads/macos/).
We recommend using the most recent supported Python version where possible.
Current installers provide a
[universal2 binary](https://en.wikipedia.org/wiki/Universal_binary) build
of Python which runs natively on all Macs (Apple Silicon and Intel) that are
supported by a wide range of macOS versions,
currently typically from at least **macOS 10.13 High Sierra** on.

The downloaded file is a standard macOS installer package file (`.pkg`).
File integrity information (checksum, size, sigstore signature, etc) for each file is included
on the release download page. Installer packages and their contents are signed and notarized
with `Python Software Foundation` Apple Developer ID certificates
to meet [macOS Gatekeeper requirements](https://support.apple.com/en-us/102445).

For a default installation, double-click on the downloaded installer package file.
This should launch the standard macOS Installer app and display the first of several
installer windows steps.

![../_images/mac_installer_01_introduction.png](../_images/mac_installer_01_introduction.png)

Clicking on the **Continue** button brings up the **Read Me** for this installer.
Besides other important information, the **Read Me** documents which Python version is
going to be installed and on what versions of macOS it is supported. You may need
to scroll through to read the whole file. By default, this **Read Me** will also be
installed in `/Applications/Python 3.13/` and available to read anytime.

![../_images/mac_installer_02_readme.png](../_images/mac_installer_02_readme.png)

Clicking on **Continue** proceeds to display the license for Python and for
other included software. You will then need to **Agree** to the license terms
before proceeding to the next step. This license file will also be installed
and available to be read later.

![../_images/mac_installer_03_license.png](../_images/mac_installer_03_license.png)

After the license terms are accepted, the next step is the **Installation Type**
display. For most uses, the standard set of installation operations is appropriate.

![../_images/mac_installer_04_installation_type.png](../_images/mac_installer_04_installation_type.png)

By pressing the **Customize** button, you can choose to omit or select certain package
components of the installer. Click on each package name to see a description of
what it installs.
To also install support for the optional experimental free-threaded feature,
see [Installing Free-threaded Binaries](#install-freethreaded-macos).

![../_images/mac_installer_05_custom_install.png](../_images/mac_installer_05_custom_install.png)

In either case, clicking **Install** will begin the install process by asking
permission to install new software. A macOS user name with `Administrator` privilege
is needed as the installed Python will be available to all users of the Mac.

When the installation is complete, the **Summary** window will appear.

![../_images/mac_installer_06_summary.png](../_images/mac_installer_06_summary.png)

Double-click on the **Install Certificates.command**
icon or file in the `/Applications/Python 3.13/` window to complete the
installation.

![../_images/mac_installer_07_applications.png](../_images/mac_installer_07_applications.png)

This will open a temporary **Terminal** shell window that
will use the new Python to download and install SSL root certificates
for its use.

![../_images/mac_installer_08_install_certificates.png](../_images/mac_installer_08_install_certificates.png)

If `Successfully installed certifi` and `update complete` appears
in the terminal window, the installation is complete.
Close this terminal window and the installer window.

A default install will include:

* A `Python 3.13` folder in your `Applications` folder. In here
  you find **IDLE**, the development environment that is a standard part of official
  Python distributions; and **Python Launcher**, which handles double-clicking Python
  scripts from the macOS [Finder](https://support.apple.com/en-us/HT201732).
* A framework `/Library/Frameworks/Python.framework`, which includes the
  Python executable and libraries. The installer adds this location to your shell
  path. To uninstall Python, you can remove these three things.
  Symlinks to the Python executable are placed in `/usr/local/bin/`.

Note

Recent versions of macOS include a **python3** command in `/usr/bin/python3`
that links to a usually older and incomplete version of Python provided by and for use by
the Apple development tools, **Xcode** or the **Command Line Tools for Xcode**.
You should never modify or attempt to delete this installation, as it is
Apple-controlled and is used by Apple-provided or third-party software. If
you choose to install a newer Python version from `python.org`, you will have
two different but functional Python installations on your computer that
can co-exist. The default installer options should ensure that its **python3**
will be used instead of the system **python3**.

### 5.1.2. How to run a Python script

There are two ways to invoke the Python interpreter.
If you are familiar with using a Unix shell in a terminal
window, you can invoke `python3.13` or `python3` optionally
followed by one or more command line options (described in [Command line and environment](cmdline.html#using-on-general)).
The Python tutorial also has a useful section on
[using Python interactively from a shell](../tutorial/appendix.html#tut-interac).

You can also invoke the interpreter through an integrated
development environment.
[IDLE — Python editor and shell](../library/idle.html#idle) is a basic editor and interpreter environment
which is included with the standard distribution of Python.
**IDLE** includes a Help menu that allows you to access Python documentation. If you
are completely new to Python, you can read the tutorial introduction
in that document.

There are many other editors and IDEs available, see [Editors and IDEs](editors.html#editors)
for more information.

To run a Python script file from the terminal window, you can
invoke the interpreter with the name of the script file:



To run your script from the Finder, you can either:

* Drag it to **Python Launcher**.
* Select **Python Launcher** as the default application to open your
  script (or any `.py` script) through the Finder Info window and double-click it.
  **Python Launcher** has various preferences to control how your script is
  launched. Option-dragging allows you to change these for one invocation, or use
  its `Preferences` menu to change things globally.

Be aware that running the script directly from the macOS Finder might
produce different results than when running from a terminal window as
the script will not be run in the usual shell environment including
any setting of environment variables in shell profiles.
And, as with any other script or program,
be certain of what you are about to run.