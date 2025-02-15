return {
	"tpope/vim-dotenv",
	event = "VimEnter",
	config = function()
		local dotenv_file = vim.fn.expand("~/.config/nvim/.env")
		if vim.fn.filereadable(dotenv_file) == 1 then
			vim.cmd("Dotenv " .. dotenv_file)
		end
	end,
}
