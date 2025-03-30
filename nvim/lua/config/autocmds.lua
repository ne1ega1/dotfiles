-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")

-- Jsonify
-- For convert python dict to JSON
vim.api.nvim_create_user_command("Jsonify", function()
	pcall(vim.api.nvim_command, "%s/'/\"/g")
	pcall(vim.api.nvim_command, "%s/True/true/g")
	pcall(vim.api.nvim_command, "%s/False/false/g")
	pcall(vim.api.nvim_command, "%s/None/null/g")
end, {})

-- Pythonify
-- For convert JSON to python dict
vim.api.nvim_create_user_command("Pythonify", function()
	pcall(vim.api.nvim_command, "%s/\"/'/g")
	pcall(vim.api.nvim_command, "%s/  /\t/g")
	pcall(vim.api.nvim_command, "%s/true/True/g")
	pcall(vim.api.nvim_command, "%s/false/False/g")
	pcall(vim.api.nvim_command, "%s/null/None/g")
end, {})
