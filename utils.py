import cv2

# символы от светлого к тёмному
ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def to_ansi_ascii(image, new_width=65):
    # конвертим в RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    # масштабируем под новую ширину
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    resized = cv2.resize(image, (new_width, new_height))

    coef = 255 / (len(ASCII_CHARS) - 1)

    ansi_image = ""
    for y in range(new_height):
        line = ""
        for x in range(new_width):
            r, g, b = resized[y, x]
            # яркость пикселя для выбора символа
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            char = ASCII_CHARS[len(ASCII_CHARS) - 1 - int(gray / coef)]
            # ANSI код цвета
            line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        ansi_image += line + "\n"
    return ansi_image

def send_key(window_id, key):
    # subprocess.run(["xdotool", "key", "--window", window_id, key])
    pass