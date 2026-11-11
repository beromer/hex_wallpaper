python -m pip install pillow

python hex_wallpaper.py \
    --width 3456 \
    --height 2234 \
    --hex-size 25 \
    --gap 1.5 \
    --shade-min 8 \
    --shade-max 45 \
    --gap-shade 65 \
    --seed 42 \
    --output wallpaper.png
    
python hex_wallpaper.py --hex-size 25 --gap 1 --shade-min 3 --shade-max 26 --gap-shade 42 --output wallpaper.png
