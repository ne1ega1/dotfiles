-- Jsonify
-- For convert python dict to JSON
vim.api.nvim_create_user_command("Jsonify", function()
	pcall(vim.api.nvim_command, '%s/\'/\"/g')
	pcall(vim.api.nvim_command, '%s/True/true/g')
	pcall(vim.api.nvim_command, '%s/False/false/g')
	pcall(vim.api.nvim_command, '%s/None/null/g')
end, {})


-- Pythonify
-- For convert JSON to python dict
vim.api.nvim_create_user_command("Pythonify", function()
	pcall(vim.api.nvim_command, '%s/\"/\'/g')
	pcall(vim.api.nvim_command, '%s/true/True/g')
	pcall(vim.api.nvim_command, '%s/false/False/g')
	pcall(vim.api.nvim_command, '%s/null/None/g')
end, {}
)
