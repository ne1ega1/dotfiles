return {
  {
    "akinsho/toggleterm.nvim",
    config = true,
    cmd = "ToggleTerm",
    keys = {
      {
        "<leader>tw", "<cmd>ToggleTerm direction=float<CR>", desc = "Toggle floating terminal"
      },
      {
        "<leader>tt", "<cmd>ToggleTerm direction=horizontal<CR>", desc = "Toggle horizontal terminal"
      },
      {
        "<leader>tv", "<cmd>ToggleTerm direction=vertical<CR>", desc = "Toggle vertical terminal"
      }
    },
    opts = {
      open_mapping = [[<C-/>]],
      direction = "horizontal",
      shade_filetypes = {},
      hide_numbers = true,
      insert_mappings = true,
      terminal_mappings = true,
      start_in_insert = true,
      close_on_exit = true
    }
  }
}
