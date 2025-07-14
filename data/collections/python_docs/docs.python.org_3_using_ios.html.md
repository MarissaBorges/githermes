### 7.1.2. Platform identification

When executing on iOS, `sys.platform` will report as `ios`. This value will
be returned on an iPhone or iPad, regardless of whether the app is running on
the simulator or a physical device.

Information about the specific runtime environment, including the iOS version,
device model, and whether the device is a simulator, can be obtained using
[`platform.ios_ver()`](../library/platform.html#platform.ios_ver "platform.ios_ver"). [`platform.system()`](../library/platform.html#platform.system "platform.system") will report `iOS` or
`iPadOS`, depending on the device.

[`os.uname()`](../library/os.html#os.uname "os.uname") reports kernel-level details; it will report a name of
`Darwin`.

### 7.1.4. Binary extension modules

One notable difference about iOS as a platform is that App Store distribution
imposes hard requirements on the packaging of an application. One of these
requirements governs how binary extension modules are distributed.

The iOS App Store requires that *all* binary modules in an iOS app must be
dynamic libraries, contained in a framework with appropriate metadata, stored
in the `Frameworks` folder of the packaged app. There can be only a single
binary per framework, and there can be no executable binary material outside
the `Frameworks` folder.

This conflicts with the usual Python approach for distributing binaries, which
allows a binary extension module to be loaded from any location on
`sys.path`. To ensure compliance with App Store policies, an iOS project must
post-process any Python packages, converting `.so` binary modules into
individual standalone frameworks with appropriate metadata and signing. For
details on how to perform this post-processing, see the guide for [adding
Python to your project](#adding-ios).

To help Python discover binaries in their new location, the original `.so`
file on `sys.path` is replaced with a `.fwork` file. This file is a text
file containing the location of the framework binary, relative to the app
bundle. To allow the framework to resolve back to the original location, the
framework must contain a `.origin` file that contains the location of the
`.fwork` file, relative to the app bundle.

For example, consider the case of an import `from foo.bar import _whiz`,
where `_whiz` is implemented with the binary module
`sources/foo/bar/_whiz.abi3.so`, with `sources` being the location
registered on `sys.path`, relative to the application bundle. This module
*must* be distributed as `Frameworks/foo.bar._whiz.framework/foo.bar._whiz`
(creating the framework name from the full import path of the module), with an
`Info.plist` file in the `.framework` directory identifying the binary as a
framework. The `foo.bar._whiz` module would be represented in the original
location with a `sources/foo/bar/_whiz.abi3.fwork` marker file, containing
the path `Frameworks/foo.bar._whiz/foo.bar._whiz`. The framework would also
contain `Frameworks/foo.bar._whiz.framework/foo.bar._whiz.origin`, containing
the path to the `.fwork` file.

When running on iOS, the Python interpreter will install an
[`AppleFrameworkLoader`](../library/importlib.html#importlib.machinery.AppleFrameworkLoader "importlib.machinery.AppleFrameworkLoader") that is able to read and
import `.fwork` files. Once imported, the `__file__` attribute of the
binary module will report as the location of the `.fwork` file. However, the
[`ModuleSpec`](../library/importlib.html#importlib.machinery.ModuleSpec "importlib.machinery.ModuleSpec") for the loaded module will report the
`origin` as the location of the binary in the framework folder.

### 7.1.5. Compiler stub binaries

Xcode doesn’t expose explicit compilers for iOS; instead, it uses an `xcrun`
script that resolves to a full compiler path (e.g., `xcrun --sdk iphoneos
clang` to get the `clang` for an iPhone device). However, using this script
poses two problems:

* The output of `xcrun` includes paths that are machine specific, resulting
  in a sysconfig module that cannot be shared between users; and
* It results in `CC`/`CPP`/`LD`/`AR` definitions that include spaces.
  There is a lot of C ecosystem tooling that assumes that you can split a
  command line at the first space to get the path to the compiler executable;
  this isn’t the case when using `xcrun`.

To avoid these problems, Python provided stubs for these tools. These stubs are
shell script wrappers around the underingly `xcrun` tools, distributed in a
`bin` folder distributed alongside the compiled iOS framework. These scripts
are relocatable, and will always resolve to the appropriate local system paths.
By including these scripts in the bin folder that accompanies a framework, the
contents of the `sysconfig` module becomes useful for end-users to compile
their own modules. When compiling third-party Python modules for iOS, you
should ensure these stub binaries are on your path.