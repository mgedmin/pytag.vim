"
" File: smart-tag.vim
" Author: Marius Gedminas <marius@gedmin.as>
" Version: 1.2
" Last Modified: 2024-11-09
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
" Does need a tags file with --extra=+f for jumping to modules
"

if !exists("g:smart_tag_python")
    if has("python3")
        let g:smart_tag_python = "python3"
    elseif has("python")
        let g:smart_tag_python = "python"
    else
        finish
    endif
endif

execute g:smart_tag_python 'import smart_tag'

fun! Tag(name)
    execute g:smart_tag_python "smart_tag.jump(vim.eval('a:name'))"
endf

command! -nargs=1 -complete=tag -bar Tag :call Tag(<f-args>)
