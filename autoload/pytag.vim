" Intended to use as :nnoremap <expr> <C-]> pytag#tag_jump_mapping()
function pytag#tag_jump_mapping()
  let line = getline(line("."))
  let [modname, startpos, endpos] = matchstrpos(line, '^\(from\|import\)\s\+\zs[a-zA-Z0-9_.]\+')
  if col(".") > startpos && col(".") <= endpos
    if exists(":Tag")
      " :Tag is provided by https://github.com/mgedmin/pytag.vim
      return ":Tag " . modname . "\<CR>"
    else
      " NB: jumping to module.py requires that you build your tags files with
      " ctags --extra=+f
      let filename = substitute(modname, '^.*[.]', '', '') . '.py'
      return ":tag " . filename . "\<CR>"
    endif
  else
    if exists(":Tag")
      " :Tag is provided by https://github.com/mgedmin/pytag.vim
      return ":Tag " . expand("<cword>") . "\<CR>"
    else
      return "\<C-]>"
    endif
  endif
endf
