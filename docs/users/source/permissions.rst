Permissions and profiles
========================

The core concept behind the access control management, is the profile.
We cannot recommend that you set permission individually(we want to preserve your sanity and
time), unless we set permission directly in one of the three profiles available in the system.

.. warning::
    Be careful when change the default permissions in any profile. Any mistake in this part of the
    system will grant permission to all users associated with the profile.

Profiles:
    Super admin:
        * Can create :ref:`project` s and :ref:`theme` s;
        * Create and link :ref:`local-admin` with :ref:`project` or :ref:`theme`;
        * Can do anything that profiles bellow can.
    Local admin:
        * Can create new :ref:`mapper` s and link them with the theme;
        * Can moderate :ref:`report` and comments;
        * Can do anything that profile bellow can.
    Mapper:
        * Can create/edit :ref:`report`;
        * Can comment on :ref:`report` s of other :ref:`mapper` s.
    Visitor:
        * Can access all public areas;
        * Can comment(as anonymous user).
