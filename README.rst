Overview
--------

This plugins provides a smarter ``:tag`` command for Python projects.

Usage::

  :Tag name                   -- jump to a global function
  :Tag class.name             -- jump to the right class method
  :Tag module.class.name      -- jump to the right class method
  :Tag module.class           -- jump to the right class
  :Tag package.module.class   -- jump to the right class
  :Tag package.module         -- jump to the right file

You still need a tags file.   What ``:Tag`` does is filter the tags according
to containing class/filename.

If you want to jump to Python modules, you'll need to generate your tags file
with the ctags option ``--extra=+f``.


Installation
------------

You need Vim with `+python` or `+python3`.

I recommend a plugin manager like Vundle_ or Pathogen_.  E.g. with Vundle
you can ::

  :PluginInstall mgedmin/pytag.vim

Manual installation:

- copy plugin/smart-tag.vim to ~/.vim/plugin/
- copy pythonx/smart_tag.py to ~/.vim/pythonx/


.. _Vundle: https://github.com/gmarik/vundle
.. _Pathogen: https://github.com/tpope/vim-pathogen
