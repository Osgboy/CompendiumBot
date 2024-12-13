import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('base', help="base path of this repository")
args = parser.parse_args()

zephon_base = Path(r'C:\Program Files (x86)\Steam\steamapps\common\ZEPHON\Data')
zephon_world_src = zephon_base / 'World'
zephon_english_src = zephon_base / 'Core' / 'Languages' / 'English'
zephon_icons_src = zephon_base / 'Video' / 'Textures' / 'Icons'

gladius_base = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Warhammer 40000 Gladius - Relics of War\Data')
gladius_world_src = gladius_base / 'World'
gladius_english_src = gladius_base / 'Core' / 'Languages' / 'English'
gladius_icons_src = gladius_base / 'Video' / 'Textures' / 'Icons'

base = Path(args.base)
zephon_world_dst = base / 'Zephon'
zephon_english_dst = base / 'Zephon' / 'English'
zephon_icons_dst = base / 'Zephon' / 'Icons'

gladius_world_dst = base / 'Gladius'
gladius_english_dst = base / 'Gladius' / 'English'
gladius_icons_dst = base / 'Gladius' / 'Icons'

src_dirs = (
    zephon_world_src, zephon_english_src, zephon_icons_src,
    gladius_world_src, gladius_english_src, gladius_icons_src,
)
dst_dirs = (
    zephon_world_dst, zephon_english_dst, zephon_icons_dst,
    gladius_world_dst, gladius_english_dst, gladius_icons_dst,
)

for src_dir, dst_dir in zip(src_dirs, dst_dirs):
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
