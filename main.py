from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    if len(binary_message) > width * height * 3:
        raise ValueError("Message is too long for the image.")
    
    index = 0
    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[index])
                    index += 1
            img.putpixel((x, y), tuple(pixel))
            if index >= len(binary_message):
                break
        if index >= len(binary_message):
            break
    
    img.save("encoded_image.png")

def decode_image(image_path):
    img = Image.open(image_path)
    binary_message = ''
    width, height = img.size
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
        if message[-1] == '\x00':
            break
    return message[:-1]

message_to_hide = "This is a secret message."
encode_image("original_image.png", message_to_hide)
decoded_message = decode_image("encoded_image.png")
print("Decoded message:", decoded_message)
