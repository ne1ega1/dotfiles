return {
	"saghen/blink.cmp",
	dependencies = {
		"Kaiser-Yang/blink-cmp-avante",
	},
	opts = {
		sources = {
			default = { "lsp", "path", "buffer", "lazydev" },
			providers = {
				lazydev = {
					name = "LazyDev",
					module = "lazydev.integrations.blink",
					score_offset = 100, -- show at a higher priority than lsp
				},
			},
		},
		keymap = {
			preset = "enter",

			["<S-Tab>"] = { "select_prev", "fallback" },
			["<Tab>"] = { "select_next", "fallback" },
			["<Esc>"] = { "hide", "fallback" },
			-- show with a list of providers
			["<C-space>"] = {
				function(cmp)
					cmp.show({ providers = { "snippets" } })
				end,
			},
		},
		completion = {
			menu = {
				border = "single",
				draw = {
					columns = {
						{ "label", "label_description", gap = 1 },
						{ "kind_icon", "kind", "source_name", gap = 1 },
					},
				},
			},
			documentation = {
				window = {
					border = "single",
				},
			},
			list = {
				selection = {
					preselect = true,
					auto_insert = false,
				},
			},
		},
	},
}
