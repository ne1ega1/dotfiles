return {
	"linux-cultist/venv-selector.nvim",
	dependencies = {
		"nvim-telescope/telescope.nvim",
		"mfussenegger/nvim-dap-python",
	},
	opts = {
		auto_select = true,
		path = "~/etlsrc",
		dap_enabled = true, -- включить интеграцию с DAP
		name = {
			"venv",
			".venv",
		},
		parents = 2, -- искать venv в родительских директориях (вверх по дереву каталогов)
	},
	event = "VeryLazy",
}
