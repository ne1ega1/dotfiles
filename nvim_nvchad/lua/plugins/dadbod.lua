return {
    "tpope/vim-dadbod",
    dependencies = {
        "kristijanhusak/vim-dadbod-ui",
        "kristijanhusak/vim-dadbod-completion",
    },
    lazy = true,
    cmd = { 'DB', 'DBUI', 'DBUIToggle', 'DBUIAddConnection' },
    -- config = function()
    --     require("plugins.dadbod").setup()
    -- end,
}

