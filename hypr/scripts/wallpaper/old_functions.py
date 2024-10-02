import sys
import toml
import subprocess

from pathlib import Path

from base_functions import load_json, dump_file

sys.path.append('/home/jumanji/.config/hypr/scripts')


def generate_alacritty_theme():
    """Конвертируем цвета из кэша в toml файл для замены цветовой схемы Alacritty"""
    json_data = load_json(Path('/home/jumanji/.cache/wal/colors.json'))

    alacritty_theme = {
        'colors': {
            'primary': {
                'foreground': json_data['special']['foreground'],
                'background': json_data['special']['background']
            },
            'cursor': {
                'cursor': json_data['special']['cursor'],
                'text': json_data['colors']['color0']
            },
            'normal': {
                'black': json_data['colors']['color0'],
                'red': json_data['colors']['color1'],
                'green': json_data['colors']['color2'],
                'yellow': json_data['colors']['color3'],
                'blue': json_data['colors']['color4'],
                'magenta': json_data['colors']['color5'],
                'cyan': json_data['colors']['color6'],
                'white': json_data['colors']['color7']
            },
            'bright': {
                'black': json_data['colors']['color8'],
                'red': json_data['colors']['color9'],
                'green': json_data['colors']['color10'],
                'yellow': json_data['colors']['color11'],
                'blue': json_data['colors']['color12'],
                'magenta': json_data['colors']['color13'],
                'cyan': json_data['colors']['color14'],
                'white': json_data['colors']['color15']
            }
        }
    }

    alacritty_theme_toml = toml.dumps(alacritty_theme)
    dump_file(Path('/home/jumanji/.config/alacritty/colors.toml'), alacritty_theme_toml)
    print(f'Theme for Alacritty successfully updated!\n')
    
    
def create_hyprlock_theme(random_wallpaper):
    """Сохраняем обои в размытом и квадратном виде для hyprlock"""
    blurred = '~/.cache/wal/blurred.png'
    square = '~/.cache/wal/square.png'
    resize_command = f'magick {random_wallpaper} -resize 75% {blurred}'
    blur_command = f'magick {blurred} -blur 50x30 {blurred}'
    square_command = f'magick {random_wallpaper} -gravity Center -extent 1:1 {square}'
    subprocess.run(resize_command, shell=True)
    subprocess.run(blur_command, shell=True)
    subprocess.run(square_command, shell=True)
    print(f'Theme for hyprlock successfully created!\n')


def set_waybar_background():
    """Подтягиваем файл CSS с цветами и меняем оформление waybar"""
    copy_command = 'cp ~/.cache/wal/colors-waybar.css ~/.config/waybar'
    subprocess.run(copy_command, shell=True)
    restart_waybar_command = '~/.config/hypr/scripts/waybar.sh'
    subprocess.run(restart_waybar_command, shell=True)


def set_swaync_colors():
    """Просто перезапускаем swaync, т.к. она в конфиге подтягивает цвета из waybar"""
    kill_command = 'pkill swaync'
    subprocess.run(kill_command, shell=True)
    start_command = 'swaync &'
    subprocess.run(start_command, shell=True)


def parse_colors(wallpaper):
    """Парсим сгенерированные цвета для изменения цветов рамок окна и использования в остальных приложениях"""
    json_data = load_json(Path('/home/jumanji/.cache/wal/colors.json'))
    result_list = [f'$wallpaper = $HOME/{"/".join(wallpaper.split("/")[3:])}\n']
    result_list.extend(
        [
            f'${color_name} = rgba({color_hex.lstrip("#")}ff)\n' for color_name, color_hex in json_data['special'].items()
        ]
    )
    result_list.extend(
        [
            f'${color_id} = rgba({color_hex.lstrip("#")}ff)\n' for color_id, color_hex in json_data['colors'].items()
        ]
    )

    with open(Path('/home/jumanji/.config/hypr/conf/hyprland_colors.conf'), 'w') as _file:
        _file.writelines(result_list)


# Подтягиваем файл CSS с цветами для waybar
subprocess.run('cp ~/.cache/wal/colors-waybar.css ~/.config/waybar', shell=True)
