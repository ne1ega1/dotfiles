require "nvchad.options"

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

require("bufferline").setup {
  options = {
    mode = "buffers",
    hover = {
      enabled = true,
      delay = 200,
      reveal = { "close" },
    },
    max_name_length = 25,
    tab_size = 20,
    separator_style = "slant",
    show_tab_indicators = true,
    offsets = {
      {
        filetype = "NvimTree",
        text = "File Explorer",
        text_align = "center",
        separator = true,
      },
    },
  },
}

-- nvim-tree
require("nvim-tree").setup {
  git = {
    enable = true,
    ignore = false,
  },
  view = {
    adaptive_size = true,
    side = "left",
    width = 35,
  },
  -- on_attach = function(bufnr)
  --     local api = require('nvim-tree.api')
  --
  --     -- Опции для маппинга клавиш
  --     local function opts(desc)
  --         return { desc = 'nvim-tree: ' .. desc, buffer = bufnr, noremap = true, silent = true, nowait = true }
  --     end
  --
  --     -- Переопределение клавиши 'l' для открытия директории
  --     vim.keymap.set('n', 'l', api.node.open.edit, opts('Open'))
  -- end,
}

-- python formatting
vim.api.nvim_create_autocmd({
  "BufNewFile",
  "BufRead",
}, {
  pattern = "*.py",
  callback = function()
    o.textwidth = 79
    o.colorcolumn = "79"
  end,
})

-- return to last edit position when opening files
vim.api.nvim_create_autocmd("BufReadPost", {
  pattern = "*",
  callback = function()
    if vim.fn.line "'\"" > 0 and vim.fn.line "'\"" <= vim.fn.line "$" then
      vim.cmd 'normal! g`"'
    end
  end,
})

-- ru simbols integrate
local function escape(str)
  local escape_chars = [[;,."|\]]
  return vim.fn.escape(str, escape_chars)
end

local en = [[qwertyuiop[]asdfghjkl;zxcvbnm,.]]
local ru = [[йцукенгшщзхъфывапролджячсмитьбю]]
local en_shift = [[QWERTYUIOP{}ASDFGHJKL:ZXCVBNM<>]]
local ru_shift = [[ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЯЧСМИТЬБЮ]]
vim.opt.langmap = vim.fn.join({ escape(ru_shift) .. ";" .. escape(en_shift), escape(ru) .. ";" .. escape(en) }, ",")

-- git conflicts resolve
vim.api.nvim_create_autocmd("User", {
  pattern = "GitConflictDetected",
  callback = function()
    vim.notify("Conflict detected in " .. vim.fn.expand "<afile>")
    vim.keymap.set("n", "cww", function()
      engage.conflict_buster()
      create_buffer_local_mappings()
    end)
  end,
})

-- noice
require("noice").setup {
  lsp = {
    -- override markdown rendering so that **cmp** and other plugins use **Treesitter**
    override = {
      ["vim.lsp.util.convert_input_to_markdown_lines"] = true,
      ["vim.lsp.util.stylize_markdown"] = true,
      ["cmp.entry.get_documentation"] = true, -- requires hrsh7th/nvim-cmp
    },
  },
  -- you can enable a preset for easier configuration
  -- presets = {
  --     bottom_search = true,         -- use a classic bottom cmdline for search
  --     command_palette = true,       -- position the cmdline and popupmenu together
  --     long_message_to_split = true, -- long messages will be sent to a split
  --     inc_rename = false,           -- enables an input dialog for inc-rename.nvim
  --     lsp_doc_border = false,       -- add a border to hover docs and signature help
  -- },
}

-- disable codeium keybindings
vim.g.codeium_disable_bindings = 1
