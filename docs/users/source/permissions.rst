PERMISSIONS:


Permissions and groups
======================
 
The main concept behind the access control management is the group (or, if you prefer, profile).
 
Basically, there are two categories of groups: the **group** itself and the **template group**. You might be wondering: what’s the difference between them?

* **group** - This is where we insert users and automatically inherits all it associated permissions.


* **template group** - It works like a permissions repository. Any permission added or removed from this template group is replicated to all associated groups. You can freely change template group permissions, but you **can’t** insert users in that group type.
 
.. warning::
Be careful when changing template permissions. Any mistake will grant or revoke permissions for all users associated with.
 
Built-in group
--------------
The VoY system automatically creates the **super admin** group. Any user in this group is virtually unlimited and can do anything in the system.
 
Built-in template
-----------------
The VoY system automatically creates two **template groups**:

Local admin template
* Can do everything that the mapper template group can do; 
* Can create mappers and link them to themes;
* Can moderate report and comments;
 
Mapper template
* Can create/edit reports;
* Can comment on reports from other mappers.

How VoY manages groups
---------------------
First, you **can’t** create groups manually or directly change permissions of a specific group.
Each project has its own **local admin group**, this group is created automatically when a new project is created and inherits all permissions from the template group **local admin template**.
 
Each theme has its own **mapper group**. This group is created automatically with new themes and will inherit all permissions from the **mapper template** group.

