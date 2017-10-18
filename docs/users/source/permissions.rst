Permissions and groups
======================

The core concept behind the access control management, is the group(or if you prefer, profile).

Basically we have two category of groups, the **group** itself and **template group**, but what is the difference
between them?

* **group** - Is where we insert users, and automatically the user inherit all permissions associated with that group.
* **template group** - Works like a repository of permissions, any permission added or removed from this template group
  is replicated to all groups associated with it. You can freely change permissions in any template group, but, you
  **cannot** insert users in this type of group.

.. warning::
    Be careful when change the permissions. Any mistake in this part of the system will grant/revoke permission to all
    users associated with that profile.

Built in group
--------------
The VoY system automatically create the group **super admin**, any user inside this group can do anything.

Built in template
-----------------
The VoY system automatically creates two **template groups**:

Local admin template
    * Can create :ref:`mapper` s and link them with the theme;
    * Can moderate :ref:`report` and comments;
    * Can do anything that mapper template group can.

Mapper template
    * Can create/edit :ref:`report`;
    * Can comment on :ref:`report` s of other :ref:`mapper` s.

How VoY manage groups
---------------------

Firstly of all, you **cannot** create groups manually neither change permissions directly to a specific group.

Each project have your own **local admin group**, this group is created automatically when a new project is created, and
inherit all permissions of the template group **local admin template**.

Each theme have your own **mapper group**, this group is created automatically when a new theme is created, and
inherit all permissions of the template group **mapper template**.
