" Intended to use as :nnoremap <expr> <C-]> pytag#tag_jump_mapping()
function pytag#tag_jump_mapping()
  let line = getline(line("."))
  let [modname, startpos, endpos] = matchstrpos(line, '^\(from\|import\)\s\+\zs[a-zA-Z0-9_.]\+')
  if col(".") > startpos && col(".") <= endpos
    return ":Tag " . modname . "\<CR>"
  else
    return ":Tag " . expand("<cword>") . "\<CR>"
  endif
endf
