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
  :Tag package                -- jump to the right file

You still need a tags file.   What ``:Tag`` does is filter the tags according
to containing class/filename.

If you want to jump to Python modules and packages, you'll need to generate
your tags file with the ctags option ``--extra=+f``.


Installation
------------

You need Vim with Python support.

I recommend a plugin manager like vim-plug_ ::

    Plug 'mgedmin/pytag.vim'

You may also want to consider the following mapping in
~/.vim/ftplugin/python.vim::

    " Smarter Ctrl-]
    nnoremap <buffer> <expr> <C-]> pytag#tag_jump_mapping()

.. _vim-plug: https://github.com/junegunn/vim-plug
