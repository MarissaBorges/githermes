2. Using Python on Unix platforms
=================================

2.1. Getting and installing the latest version of Python
--------------------------------------------------------

### 2.1.1. On Linux

Python comes preinstalled on most Linux distributions, and is available as a
package on all others. However there are certain features you might want to use
that are not available on your distro’s package. You can compile the
latest version of Python from source.

In the event that the latest version of Python doesn’t come preinstalled and isn’t
in the repositories as well, you can make packages for your own distro. Have a
look at the following links:

#### 2.1.1.1. Installing IDLE

In some cases, IDLE might not be included in your Python installation.

* For Debian and Ubuntu users:

  ```
  sudo apt update
  sudo apt install idle

  ```
* For Fedora, RHEL, and CentOS users:

  ```
  sudo dnf install python3-idle

  ```
* For SUSE and OpenSUSE users:

  ```
  sudo zypper install python3-idle

  ```
* For Alpine Linux users:

  ```
  sudo apk add python3-idle

  ```

### 2.1.2. On FreeBSD and OpenBSD

* FreeBSD users, to add the package use:
* OpenBSD users, to add the package use:

  ```
  pkg_add -r python

  pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/<insert your architecture here>/python-<version>.tgz

  ```

  For example i386 users get the 2.5.1 version of Python using:

  ```
  pkg_add ftp://ftp.openbsd.org/pub/OpenBSD/4.2/packages/i386/python-2.5.1p2.tgz

  ```

2.2. Building Python
--------------------

If you want to compile CPython yourself, first thing you should do is get the
[source](https://www.python.org/downloads/source/). You can download either the
latest release’s source or just grab a fresh [clone](https://devguide.python.org/setup/#get-the-source-code). (If you want
to contribute patches, you will need a clone.)

The build process consists of the usual commands:

```
./configure
make
make install

```

[Configuration options](configure.html#configure-options) and caveats for specific Unix
platforms are extensively documented in the [README.rst](https://github.com/python/cpython/tree/3.13/README.rst) file in the
root of the Python source tree.

Warning

`make install` can overwrite or masquerade the `python3` binary.
`make altinstall` is therefore recommended instead of `make install`
since it only installs `exec_prefix/bin/pythonversion`.

2.4. Miscellaneous
------------------

To easily use Python scripts on Unix, you need to make them executable,
e.g. with

and put an appropriate Shebang line at the top of the script. A good choice is
usually

which searches for the Python interpreter in the whole `PATH`. However,
some Unices may not have the **env** command, so you may need to hardcode
`/usr/bin/python3` as the interpreter path.

To use shell commands in your Python scripts, look at the [`subprocess`](../library/subprocess.html#module-subprocess "subprocess: Subprocess management.") module.

2.5. Custom OpenSSL
-------------------

1. To use your vendor’s OpenSSL configuration and system trust store, locate
   the directory with `openssl.cnf` file or symlink in `/etc`. On most
   distribution the file is either in `/etc/ssl` or `/etc/pki/tls`. The
   directory should also contain a `cert.pem` file and/or a `certs`
   directory.

   ```
   $ find /etc/ -name openssl.cnf -printf "%h\n"
   /etc/ssl

   ```
2. Download, build, and install OpenSSL. Make sure you use `install_sw` and
   not `install`. The `install_sw` target does not override
   `openssl.cnf`.

   ```
   $ curl -O https://www.openssl.org/source/openssl-VERSION.tar.gz
   $ tar xzf openssl-VERSION
   $ pushd openssl-VERSION
   $ ./config \
       --prefix=/usr/local/custom-openssl \
       --libdir=lib \
       --openssldir=/etc/ssl
   $ make -j1 depend
   $ make -j8
   $ make install_sw
   $ popd

   ```
3. Build Python with custom OpenSSL
   (see the configure `--with-openssl` and `--with-openssl-rpath` options)

   ```
   $ pushd python-3.x.x
   $ ./configure -C \
       --with-openssl=/usr/local/custom-openssl \
       --with-openssl-rpath=auto \
       --prefix=/usr/local/python-3.x.x
   $ make -j8
   $ make altinstall

   ```

Note

Patch releases of OpenSSL have a backwards compatible ABI. You don’t need
to recompile Python to update OpenSSL. It’s sufficient to replace the
custom OpenSSL installation with a newer version.