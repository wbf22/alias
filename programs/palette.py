import random

def generate_palette(num_colors=5):
    base_hue = random.randint(0, 360)
    harmony_type = random.choice(["complementary", "analogous", "triadic", "tetradic"])
    hues = []
    if harmony_type == "complementary":
        hues = [base_hue, (base_hue + 180) % 360]
    elif harmony_type == "analogous":
        hues = [base_hue, (base_hue + 30) % 360, (base_hue - 30) % 360]
    elif harmony_type == "triadic":
        hues = [base_hue, (base_hue + 120) % 360, (base_hue + 240) % 360]
    elif harmony_type == "tetradic":
        hues = [base_hue, (base_hue + 60) % 360, (base_hue + 180) % 360, (base_hue + 240) % 360]

    # Generate additional colors by slightly varying primary hues
    print(f"\033[0mHarmony: {harmony_type}")
    palette_hues = []
    palette_hues.extend(hues)
    for i in range(num_colors - len(hues)):
        hue = palette_hues[random.randint(0, len(palette_hues)-1)]
        slight_variation = random.uniform(-20, 20)
        new_hue = (hue + slight_variation) % 360
        palette_hues.append(new_hue)

    # Trim to the desired number of colors
    palette_hues = palette_hues[:num_colors]

    # Convert hues to RGB
    palette = [tuple(int(c * 255) for c in hsv_to_rgb(h, random.uniform(0.0, 1.0), random.uniform(0.0, 1.0))) for h in palette_hues]

    return palette

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = v - c
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return r + m, g + m, b + m


def print_palette(palette):
    for idx, (r, g, b) in enumerate(palette, 1):
        hex_value = f"#{r:02X}{g:02X}{b:02X}"
        print(f"\033[48;2;{r};{g};{b}m     \033[0m \033[38;2;{r};{g};{b}m{hex_value} RGB({r}, {g}, {b})\033[0m")
        print(f"\033[48;2;{r};{g};{b}m     \033[0m")

if __name__ == "__main__":
    while True:
        palette = generate_palette()
        print_palette(palette)
        input("Hit Enter to generate new colors or Ctrl+C to exit...")