Terms
=====

.. _project:

Project
-------
The project is the grate data aggregator, besides users, groups and profiles, nothing can exists without a project.
Each project have a region where one or more :ref:`theme` s can be created.

.. _theme:

Theme
-----
Theme is which object of study has been maded by :ref:`mapper`.

Each project can have one or more themes actives at same time, where each one have a boundry region.

.. warning::
    The boundry region of each theme must be inside the same region configured inside the :ref:`project`.

.. _report:

Report
------
Report is the heart of the VoY, a report can contains text, images and links, and can be created by users with this profiles: :ref:`admin`, :ref:`local-admin` and :ref:`mapper`

.. _mapper:

Mapper
------
Mapper is the young people that can create :ref:`report` s.

.. note::
    The mapper must be registered in VoY system before create a report.

.. note::
    The mapper only can create report inside the boundry region configured on :ref:`theme`.

.. note::
    Only :ref:`admin` or `local-admin` can create then.

.. _admin:

Admin
-----
Admin is a jedi master. Only users with this profile can manage the projects.

.. _local-admin:

Local admin
-----------
Local admin is the person(s) can manage :ref:`theme` and :ref:`mapper`.
