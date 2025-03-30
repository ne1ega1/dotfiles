local o = vim.o

o.encoding = "utf-8"
o.cursorlineopt = "both"
o.nu = true
o.relativenumber = true

o.tabstop = 4
o.softtabstop = 4
o.shiftwidth = 4
o.expandtab = true -- convert tabs to spaces
o.autoindent = true -- auto indentation
o.list = true -- show tab characters and trailing whitespace
o.ignorecase = true -- ignore case when searching
o.smartcase = true -- unless capital letter in search
o.hlsearch = false -- do not highlight all matches on previous search pattern
o.incsearch = true -- incrementally highlight searches as you type
o.termguicolors = true -- enable true color support
o.scrolloff = 8 -- minimum number of lines to keep above and below the cursor
o.sidescrolloff = 8 --minimum number of columns to keep above and below the cursor
o.termguicolors = true --bufferline
o.textwidth = 120 -- maximum width of text
o.wrap = false -- disable line wrapping
o.colorcolumn = "120" -- highlight column 120

-- LazyVim auto format
vim.g.autoformat = false

-- disable Ruff
vim.g.lazyvim_python_ruff = ""

-- add source path
vim.g.lazyvim_pyright_extra_paths = { "/home/jumanji/etlsrc/airflow/src" }

-- disable codeium keybindings
-- vim.g.codeium_disable_bindings = 1

vim.g.matchup_enabled = 1
