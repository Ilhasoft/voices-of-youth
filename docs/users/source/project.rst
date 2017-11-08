Project
=======

The project is the entry point.

When create a new project, you can see these fields:
    * name - The name of the project;
    * description - Some description about the project;
    * url path - The path that will be used to access the project in browser URL. e.g.
      **www.voicesofyouth.org/project-path** if this field is not informed the system will
      generate a slugify version of project name;
    * language - The main language used in this project. We'll show you how to add new languages;
    * window title - The title used in browser window/tab.
    * tags - Tags that user can use when create a new report in any theme linked with this project.

.. note::
    * Only admins or local admins can create or edit themes and add mappers to these theme;
    * You can create as many themes as you need;
    * You can create more than one theme in the same boundary region of others themes. e.g. One study about health risks
      and another about security issues.

.. warning::
    The border region of each theme must be within the same region configured in the :term:`project`. This boundary theme
    region may be smaller than the project boundary, but may never be larger or be outside of the project area.

.. todo::
    Add section to teach how to add new language.
