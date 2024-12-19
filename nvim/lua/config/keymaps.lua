local map = vim.keymap.set

-- Base
map("n", ";", ":", { desc = "CMD enter command mode" })
map("n", "<leader>w", ":w<CR>", { desc = "Save" })
map("i", "jj", "<Esc>", { desc = "Exit in insert mode" })
-- map({ "n", "v" }, "<leader>y", [["+y]], { desc = "Yank to clipboard" })
-- map({ "n", "i", "v" }, "<C-s>", "<cmd> w <cr>")

-- Navigation
map("n", "<c-k>", ":wincmd k<CR>")
map("n", "<c-j>", ":wincmd j<CR>")
map("n", "<c-h>", ":wincmd h<CR>")
map("n", "<c-l>", ":wincmd l<CR>")

-- Splits
map("n", "\\", ":vsplit<CR>", { desc = "Vertical split" })
map("n", "|", ":split<CR>", { desc = "Horizontal split" })
map("n", "<leader>sx", "<cmd>close<CR>", { desc = "Close current split window" })

-- Tabs
map("n", "<Tab>", ":bn<CR>", { desc = "Next tab" })
map("n", "<s-Tab>", ":bp<CR>", { desc = "Previous tab" })
map("n", "<leader>x", ":BufferLinePickClose<CR>", { desc = "Close active tab" })
map("n", "<leader>X", ":BufferLineCloseRight<CR>", { desc = "Close right tab" })
map("n", "<leader>s", ":BufferLineSortByTabs<CR>", { desc = "Sorting tabs by name" })

-- Terminal
map("n", "<leader>dd", ':TermExec cmd="sudo systemctl start docker.socket"', { desc = "Start docker" })
map("n", "<leader>mu", ':TermExec cmd="make up" direction=float<CR>', { desc = "Start airflow" })
map("n", "<leader>md", ':TermExec cmd="make down" direction=float<CR>', { desc = "Stop airflow" })
map(
  "n",
  "<leader>mr",
  ':TermExec cmd="make down && make clean && make up" direction=float<CR>',
  { desc = "Restart airflow" }
)
map(
  "n",
  "<leader>mb",
  ':TermExec cmd="make build/airflow && make build/crawlers && make build/parsers/base && make build/normalizers/base" direction=float<CR>',
  { desc = "Build base" }
)
map(
  "n",
  "<leader>mo",
  ':TermExec cmd="make build/xporters/couchdb && make build/joiners && make build/operators" direction=float<CR>',
  { desc = "Build operators" }
)

-- Codeium
map("i", "<C-g>", function()
  return vim.fn["codeium#Accept"]()
end, { expr = true, silent = true })
map("i", "<c-;>", function()
  return vim.fn["codeium#CycleCompletions"](1)
end, { expr = true, silent = true })
map("i", "<c-,>", function()
  return vim.fn["codeium#CycleCompletions"](-1)
end, { expr = true, silent = true })
map("i", "<c-x>", function()
  return vim.fn["codeium#Clear"]()
end, { expr = true, silent = true })
