return {
    'akinsho/bufferline.nvim',
    version = "*",
    dependencies = 'nvim-tree/nvim-web-devicons',
    config = function()
        require('bufferline').setup(
            {
                options = {
                    max_name_length = 25,
                    tab_size = 22,
                    separator_style = "slope"
                }
            }
        )
    end,
}
