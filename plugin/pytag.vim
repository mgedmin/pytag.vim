"
" File: pytag.vim
" Author: Marius Gedminas <marius@gedmin.as>
" Version: 2.0
" Last Modified: 2024-11-12
"
" Smarter :tag
"
" Usage:
"   :Tag name                   -- jump to a global function
"   :Tag class.name             -- jump to the right class method
"   :Tag module.class.name      -- jump to the right class method
"   :Tag module.class           -- jump to the right class
"   :Tag package.module.class   -- jump to the right class
"   :Tag package.module         -- jump to the right file
"
" What the :Tag command does is search for tags matching the last part of a
" dotted name, and then filter them according to containing class/filename.
"
" Needs vim with Python support (because vimscript is painful to work in).
"
" Doesn't need a tags file with --extra=+q (which stopped working for Python
" anyway in some exuberant ctags version).
"
" Need a tags file with --extra=+f for jumping to modules.
"

pyx import pytag

fun! s:Tag(name)
    pyx pytag.jump(vim.eval('a:name'))
endf

command! -nargs=? -complete=tag -bar  Tag  call s:Tag(<q-args>)
