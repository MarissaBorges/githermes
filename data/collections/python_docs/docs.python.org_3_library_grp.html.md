`grp` — The group database
==========================

---

This module provides access to the Unix group database. It is available on all
Unix versions.

Group database entries are reported as a tuple-like object, whose attributes
correspond to the members of the `group` structure (Attribute field below, see
`<grp.h>`):

| Index | Attribute | Meaning |
| --- | --- | --- |
| 0 | gr\_name | the name of the group |
| 1 | gr\_passwd | the (encrypted) group password; often empty |
| 2 | gr\_gid | the numerical group ID |
| 3 | gr\_mem | all the group member’s user names |

The gid is an integer, name and password are strings, and the member list is a
list of strings. (Note that most users are not explicitly listed as members of
the group they are in according to the password database. Check both databases
to get complete membership information. Also note that a `gr_name` that
starts with a `+` or `-` is likely to be a YP/NIS reference and may not be
accessible via [`getgrnam()`](#grp.getgrnam "grp.getgrnam") or [`getgrgid()`](#grp.getgrgid "grp.getgrgid").)

It defines the following items:

grp.getgrgid(*id*)
:   Return the group database entry for the given numeric group ID. [`KeyError`](exceptions.html#KeyError "KeyError")
    is raised if the entry asked for cannot be found.

    Changed in version 3.10: [`TypeError`](exceptions.html#TypeError "TypeError") is raised for non-integer arguments like floats or strings.

grp.getgrnam(*name*)
:   Return the group database entry for the given group name. [`KeyError`](exceptions.html#KeyError "KeyError") is
    raised if the entry asked for cannot be found.

grp.getgrall()
:   Return a list of all available group entries, in arbitrary order.

See also

Module [`pwd`](pwd.html#module-pwd "pwd: The password database (getpwnam() and friends). (Unix)")
:   An interface to the user database, similar to this.