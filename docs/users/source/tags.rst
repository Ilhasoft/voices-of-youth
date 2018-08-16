Tag
===

A report made by a mapper has a tag field, but the user can’t create new tags. Instead, the user selects only the tags created previously by the super admin or local admin.

These tags come from two different places: ref: `project` or theme.

When a global-admin creates a tag for the project, all reports for all themes can use this tag.
When a global-admin or local-admin creates a tag for the theme, any report created for that theme can use this tag.

The tag isn’t required when you create a new project, theme, or report.

..note::
    If you create a new tag for a project or theme, any report created before this tag can use it.
