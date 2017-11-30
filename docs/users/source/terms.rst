Terms
=====

.. _voy:

Voices of Youth(VoY)
--------------------
To simplify your overview of VoY, let's make a simple analogy:

Think of VoY as a large file cabinet with several drawers, where each drawer is a project and inside this drawer we can
save several file folders, these folders are the themes and the files inside these folders are the reports.

.. _project:

Project
-------
The project is a great data aggregator, besides users, groups and profiles, nothing can exists without a project.
Each project have a region where one or more :ref:`theme` s can be created.

.. note::
    Only :ref:`admin` can manage projects.

.. _theme:

Theme
-----
A theme is used to create a study around a subject. Each theme have your own boundry region, where the :ref:`mapper`
can create your :ref:`report`.

.. note::
    * Only :ref:`admin` or :ref:`local-admin` can manage themes;
    * Only :ref:`admin` or :ref:`local-admin` manage mappers;
    * You can create as many themes as you need;
    * You can create more than one theme in the same boundary region of others themes. e.g. One study about health risks
      and another about security issues.

.. warning::
    The border region of each theme must be within the same region configured in the :ref:`project`. This boundary theme
    region may be smaller than the project boundary, but may never be larger or be outside of the project area.

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

Global admin
------------
Global admin is a jedi master. Only users with this profile can manage the projects and :ref:`local-admin`.

.. _local-admin:

Local admin
-----------
Local admin is the person(s) can manage :ref:`theme` and :ref:`mapper`.
