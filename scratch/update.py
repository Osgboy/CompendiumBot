import os, shutil

zephon_world_src = r'C:\Program Files (x86)\Steam\steamapps\common\ZEPHON Demo\Data\World'
zephon_english_src = r'C:\Program Files (x86)\Steam\steamapps\common\ZEPHON Demo\Data\Core\Languages\English'
zephon_icons_src = r'C:\Program Files (x86)\Steam\steamapps\common\ZEPHON Demo\Data\Video\Textures\Icons'

gladius_world_src = r'C:\Program Files\Epic Games\Warhammer40KGladius\Data\World'
gladius_english_src = r'C:\Program Files\Epic Games\Warhammer40KGladius\Data\Core\Languages\English'
gladius_icons_src = r'C:\Program Files\Epic Games\Warhammer40KGladius\Data\Video\Textures\Icons'

zephon_world_dst = r'C:\Users\Oliver\Downloads\GladiusBot\Zephon'
zephon_english_dst = r'C:\Users\Oliver\Downloads\GladiusBot\Zephon\English'
zephon_icons_dst = r'C:\Users\Oliver\Downloads\GladiusBot\Zephon\Icons'

gladius_world_dst = r'C:\Users\Oliver\Downloads\GladiusBot\Gladius'
gladius_english_dst = r'C:\Users\Oliver\Downloads\GladiusBot\Gladius\English'
gladius_icons_dst = r'C:\Users\Oliver\Downloads\GladiusBot\Gladius\Icons'

src_dirs = (zephon_world_src, zephon_english_src, zephon_icons_src, gladius_world_src, gladius_english_src, gladius_icons_src)
dst_dirs = (zephon_world_dst, zephon_english_dst, zephon_icons_dst, gladius_world_dst, gladius_english_dst, gladius_icons_dst)

for src_dir, dst_dir in zip(src_dirs, dst_dirs):
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)