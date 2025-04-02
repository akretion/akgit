akgit: Git helper for akretion
=========================

Description
-------------

Akgit will run some command before running git (and solve some recurrent user mistake)


commit
~~~~~~~~

- Install pre-commit automatically if a configuration exists


Push
~~~~~~

- Automatically add akretion remote based on origin url
- Block direct push top OCA and Shopinvader

Clone
~~~~~

- Use git-autoshare


Fetch
~~~~~~~~~

- Before fetch check if the remote exist and if not add it automatically. (You can use alias for following company: ak=>akretion, c2c=>camptocamp, acs=>acsone

Install
---------

.. code-block:: shell

   pipx install git+https://github.com/akretion/akgit --force --include-deps


Configure git-autoshare
-------------------------

Edit the file .config/git-autoshare/repos.yml and put the following content

.. code-block:: shell

   github.com:
       "*":
           orgs:
               - odoo
               - OCA
               - akretion
           private: True
