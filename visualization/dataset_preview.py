import os
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def clean_filename(filename):
    cleaned = re.sub(r'_\d+\.tiff$', '', filename)
    cleaned = cleaned.replace('.', '')
    return cleaned

def create_animation_with_pil(input_dir: str, output_path: str, frame_duration_ms: int = 500):
    tiff_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.tiff')])
    selected_files = tiff_files[::10]

    try:
        font = ImageFont.load_default()
    except:
        font = None

    pil_frames = []
    for filename in selected_files:
        img_path = os.path.join(input_dir, filename)

        # Cargar imagen TIFF de 16 bits y normalizar a 8 bits
        img_16bit = Image.open(img_path)
        img_np = np.array(img_16bit)
        img_norm = ((img_np.astype(np.float32) / 65535.0) * 255).astype(np.uint8)

        pil_img = Image.fromarray(img_norm, mode='L').convert('RGB')

        # Dibujar texto
        draw = ImageDraw.Draw(pil_img)
        text = clean_filename(filename)
        x, y = 10, 10
        border_color = 'black'
        text_color = 'white'

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, fill=border_color, font=font)

        draw.text((x, y), text, fill=text_color, font=font)

        pil_frames.append(pil_img)

    pil_frames[0].save(
        output_path,
        save_all=True,
        append_images=pil_frames[1:],
        duration=frame_duration_ms,
        loop=0
    )
    print(f"GIF: {output_path}")

if __name__ == '__main__':
    input_directory = "data/pure_aberrations/raw"
    output_gif = "visualization/gifs/pure_aberrations_preview.gif"
    os.makedirs(os.path.dirname(output_gif), exist_ok=True)

    create_animation_with_pil(input_directory, output_gif)
