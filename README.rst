Git helper for akretion
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



Install
---------


.. code-block:: shell

   pipx install -e . --force --include-deps


Then add an alias for mapping into bashrc


.. code-block:: shell

   alias git='akgit'
