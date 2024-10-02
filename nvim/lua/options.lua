require "nvchad.options"

local o = vim.o

o.encoding = "utf-8"
o.cursorlineopt = 'both'
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
require("bufferline").setup{} --bufferline

vim.api.nvim_create_autocmd(
  {
    "BufNewFile",
    "BufRead"
  },
  {
  pattern = "*.py",
  callback = function()
    o.textwidth = 79
    o.colorcolumn = "79"
  end
  }
) -- python formatting

vim.api.nvim_create_autocmd("BufReadPost", {
    pattern = "*",
    callback = function()
      if vim.fn.line("'\"") > 0 and vim.fn.line("'\"") <= vim.fn.line("$") then
        vim.cmd("normal! g`\"")
      end
    end
}) -- return to last edit position when opening files

