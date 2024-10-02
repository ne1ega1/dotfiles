#!/usr/bin/env python

import os
import sys
import random
import argparse
import subprocess

sys.path.append('/home/jumanji/.config/hypr/scripts')


def select_wallpaper(wallpapers):
    """Выбираем обои в rofi"""
    rofi_input = ""
    random.shuffle(wallpapers)
    
    for wall in wallpapers:
        rofi_input += f"{wall}\x00icon\x1f{wall}\n"
    
    rofi_command = ["rofi", "-dmenu", "-i", "-replace", "-config", os.path.expanduser("~/.config/rofi/wallpaper-select.rasi")]
    result = subprocess.run(
        rofi_command,
        input=rofi_input.encode(),
        stdout=subprocess.PIPE
    )
    selected_wallpaper = result.stdout.decode().strip()

    if selected_wallpaper:
        print(f'Wallpaper selected: {selected_wallpaper.split("/")[-1]}')
        return selected_wallpaper


def set_wallpaper(wallpaper):
    """Устанавливаем обои"""
    subprocess.run(
        f'swww img {wallpaper} --transition-bezier .43,1.19,1,.4 --transition-fps=60 '
        f'--transition-type="random" --transition-duration=0.7 --transition-pos "$( hyprctl cursorpos )"',
        shell=True
    )
    print(f'Wallpaper {wallpaper} successfully updated!')


def save_colors_to_cache(wallpaper):
    """Сохраняем цвета в кэш"""
    command_get_colors = f'wal -i {wallpaper}'
    subprocess.run(
        command_get_colors,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    ).stdout.decode().split('\n')
    print('Colors has been saved in cache!')


def create_blur_wallpaper(wallpaper):
    """Сохраняем размытую копию обоев для Hyprlock"""
    subprocess.run(f'magick {wallpaper} -blur 50x30 ~/.cache/wal/blurred.png', shell=True)
    print(f'Theme for hyprlock successfully created!\n')


def main(mode):
    """Скрипт для установки обоев и цветовых схем для приложений на их основе"""
    wallpapers_dir = os.path.expanduser('~/Pictures/wallpapers')
    wallpapers = [os.path.join(wallpapers_dir, _file) for _file in os.listdir(wallpapers_dir) if _file.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if mode == 'select':
        # Выбираем обои из списка
        wallpaper = select_wallpaper(wallpapers)
        #subprocess.run("rofi -theme fullscreen-preview.rasi -show filebrowser -filebrowser-command 'feh --bg-scale' -filebrowser-directory ~/Pictures/wallpapers/", shell=True)
    else:
        # Выбираем рандомные обои
        wallpaper = random.choice(wallpapers)

    # Устанавливаем их
    set_wallpaper(wallpaper)
    # Сохраняем цвета в кэш
    save_colors_to_cache(wallpaper)
    # Создаем цветовую схему для Telegram
    subprocess.run('walogram', shell=True)
    print(f'Theme for Telegram successfully created!\n')
    # Перезапускаем swaync для обновления цветовой палитры
    subprocess.run('pkill swaync && swaync &', shell=True)
    # Сохраняем размытую копию обоев для Hyprlock
    create_blur_wallpaper(wallpaper)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Select or random choice a wallpaper.")
    parser.add_argument("--mode", type=str, required=True, help="Select mode")
    args = parser.parse_args()
    main(args.mode)
    print('All operation completed successfully!')
