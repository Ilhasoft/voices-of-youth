Terms
=====
 
.. _voy:
 
Voices of Youth(VoY)
--------------------
To simplify your VoY overview, let's take a simple analogy:
 
Think of VoY as a large file with multiple drawers, where each drawer is a project and inside this drawer, we can save several file folders, these folders are the themes and files, and inside these folders are the reports.
 
.. _project:
 
Project
-------
The project is a great aggregator of data, beyond users, groups, and profiles, nothing can exist without a project.
Each project has a region where one or more: ref: `theme`s can be created.
.. note::
   Only :ref:`admin` can manage projects.

.. _theme:
 
Theme
-----
A theme is used to create a study around a subject. Each theme has its own boundary region, where the: ref: `mapper` can create his: ref: `reports`.
.. note::
* Only: ref: `admin` or: ref:` local-admin` can manage themes;
* Only: ref: `admin` or: ref:` local-admin` manage the mappers;
* You can create as many themes as you need;
* You can create more than one theme in the same border region as other themes. For example a study on health risks and another on safety issues.
.. warning::
The border region of each theme must be within the same region configured in :ref: `project`. This border region may be smaller than the project boundary, but it can never be larger or outside of the project area.
 
.. _report:
 
Report
------
 
The report is the heart of VoY, a report can contain text, images, videos and links. It can be created by the following user profiles: ref: `admin`,: ref:` local-admin` e: ref: `mapper`
 
.. _mapper:
 
Mapper
------
Mapper is the young people who can create: ref: `report`s.
 
.. note::
The mapper must be registered in the VoY system before creating a report.
.. note::

The mapper can only create a report within the border region configured in :ref: `theme`.
.. note::
 
Only: ref: `admin` or` local-admin` can create them.
 
.. _admin:
 
Global admin
------------
Global admin is a Jedi master. Only users with this profile can manage projects and :ref: `local-admin`.

.. _local-admin:
 
Local admin
-----------
Local admin is the people who can manage: ref: `theme` e: ref:` mapper`.

