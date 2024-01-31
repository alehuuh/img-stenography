from PIL import Image
import os


def is_valid_inputs(menu_input):
    menu_list = ["encrypt", "decrypt", "exit"]
    if menu_input not in menu_list:
        return False
    return True

def is_valid_image_file(filename):
    if os.path.exists(filename):
        if filename.endswith((".jpg", ".jpeg")):
            return True
    else:
        return False

def load_image_data(filename):
    image = Image.open(filename)
    size = image.size
    image_data = image.getdata()
    return size , list(image_data)

def save_image_to_file(filename, image_dimension, image_data):
    image = Image.new("RGB", image_dimension)
    image.putdata(image_data)
    return image.save(filename, format="png")

def is_valid_key(key):
    key_list = ["u", "d"]
    if 3 <= len(key) <= 20:
        for x in range(0, len(key)):
            if key[x] not in key_list:
                return False
            else:
                x += 1
        return True
    else:
        return False

def is_valid_message(message):
    if 10 <= len(message) <= 1000:
        for x in range(0, len(message)):
            if not chr(32) <= message[x] <= chr(126):
                return False
            else:
                x += 1
        return True
    else:
        return False


def get_data_to_encrypt(image_size):
    secret_key = input("Enter Key:")
    message = input("Enter Message:")

    while not is_valid_key(secret_key) or not is_valid_message(message):
        print ("Invalid Key/Message. Please Try again.")
        secret_key = input("Enter Key:")
        message = input("Enter Message:")

    if is_valid_key(secret_key) and is_valid_message(message):
        char_in_bits = (len(secret_key) + len(message)) * 8
        image_pixels = image_size[0] * image_size[1]
        required_pixels = 6 + (char_in_bits // 3)

        while image_pixels < required_pixels:
            print ("Message and Key cannot fit in the image.")
            secret_key = input("Enter Key:")
            message = input("Enter Message:")

            while not is_valid_key(secret_key) or not is_valid_message(message):
                print ("Invalid Key/Message. Please Try again.")
                secret_key = input("Enter Key:")
                message = input("Enter Message:")

            if is_valid_key(secret_key) and is_valid_message(message):
                char_in_bits = (len(secret_key) + len(message)) * 8
                image_pixels = image_size[0] * image_size[1]
                required_pixels = 6 + (char_in_bits // 3)

        if image_pixels > required_pixels:
            return (secret_key , message)


def encrypt_text(key, text):
    encrypted_text = ''
    no_char_key = len(key)

    for x in range(0, len(text)):
        letter_decimal = ord(text[x])

        if x >= len(key):
            char_key = key[x % len(key)]
        else:
            char_key = key[x]

        if char_key == "u":
            letter_decimal = letter_decimal + no_char_key
            if letter_decimal > 126:
                letter_decimal = (letter_decimal - 32) % len(range(32,127)) + 32

        else:
            letter_decimal = letter_decimal - no_char_key
            if letter_decimal < 32:
                letter_decimal = (letter_decimal - 32) % len(range(32,127)) + 32

        encrypted_text = encrypted_text + chr(letter_decimal)
    return encrypted_text

def char_to_ascii(word):
    ascii_values= []
    for value in word:
        converted_value = ''
        converted_value = ord(value)
        ascii_values.append(converted_value)
    return ascii_values

def ascii_to_binary(ascii_values):
    binary_values= []
    for value in ascii_values:
        converted_value = ''
        converted_value = bin(value)[2:]
        while len(converted_value) < 8:
            converted_value = "0" + converted_value
        binary_values.append(converted_value)
    return binary_values

def encode_message(image_data, binary_key, binary_encrypted_message):
    binary_key.append('11111111')
    binary_encrypted_message.append('11111111')
    new_binary_key = ''.join(binary_key)
    new_binary_message = ''.join(binary_encrypted_message)
    binary_list = new_binary_key + new_binary_message
    binary_index = 0
    modified_image_data = []
    binary_len = len(binary_list)

    for rgb_values in image_data:
        list_rgb = list(rgb_values)
        new_rgb = []
        for pixel in list_rgb:
            if binary_index < binary_len:
                if (pixel %2) != 0:
                    if binary_list[binary_index] == "0":
                        pixel = pixel - 1
                        new_rgb.append(pixel)
                        binary_index += 1
                    else:
                        new_rgb.append(pixel)
                        binary_index += 1

                else:
                    if binary_list[binary_index] == "1":
                        pixel = pixel + 1
                        new_rgb.append(pixel)
                        binary_index += 1
                    else:
                        new_rgb.append(pixel)
                        binary_index += 1
            else:
                new_rgb.append(pixel)

        modified_image_data.append(tuple(new_rgb))
        new_rgb = []
    del image_data [:]
    image_data.extend(modified_image_data)

    return image_data

def decode_message(image_data):
    binary_index = 0
    binary_data = []
    binary_data_initial = ""
    delimiter = "11111111"

    for rgb_values in image_data:
        for pixel in rgb_values:
            if len(binary_data_initial) != 8:
                if (pixel % 2) != 0:
                        binary_data_initial = binary_data_initial + '1'
                        binary_index += 1

                else:
                        binary_data_initial = binary_data_initial + '0'
                        binary_index += 1

            else:
                n_binary_data_initial = ''.join(binary_data_initial)
                binary_data.append(n_binary_data_initial)
                binary_data_initial = ""

                if (pixel % 2) != 0:
                        binary_data_initial = binary_data_initial + '1'
                        binary_index += 1

                else:
                        binary_data_initial = binary_data_initial + '0'
                        binary_index += 1

    extracted_binary_data, binary_list, delimiter_list = [], [], []

    if delimiter in binary_data:
        for x in binary_data:
            if len(delimiter_list) < 2:
                if x == delimiter:
                    delimiter_list.append(x)
                    extracted_binary_data.append(binary_list)
                    binary_list = []
                else:
                    binary_list.append(x)

        if len(delimiter_list) == 2:

            binary_key, binary_encrypted_message = extracted_binary_data
            return tuple((binary_key, binary_encrypted_message))
        else:
            return (None, None)
    else:
        return (None, None)

def binary_to_ascii_string(binary_values):

    binary_string = ''

    for x in binary_values:
        output = chr(int(x,2))
        binary_string = binary_string + output

    return binary_string


def decrypt_text(encrypted_text, key):
    decrypted_text = ''
    no_char_key = len(key)

    for x in range(0, len(encrypted_text)):
        letter_decimal = ord(encrypted_text[x])

        if x >= len(key):
            char_key = key[x % len(key)]
        else:
            char_key = key[x]

        if char_key == "d":
            letter_decimal = letter_decimal + no_char_key
            if letter_decimal > 126:
                letter_decimal = (letter_decimal - 32) % len(range(32,127)) + 32

        else:
            letter_decimal = letter_decimal - no_char_key
            if letter_decimal < 32:
                letter_decimal = (letter_decimal - 32) % len(range(32,127)) + 32

        decrypted_text = decrypted_text + chr(letter_decimal)
    return decrypted_text

def save_file(filename, text):
    with open(filename, 'w') as file:
            file.write(text)

def main():
    user_input = input("Select program mode: (encrypt/decrypt/exit):")

    while not is_valid_inputs(user_input):
        print ("Invalid input, choose a different item!")
        user_input = input("Select program mode: (encrypt/decrypt/exit):")

    while not user_input == "exit":

        if user_input == "encrypt":
            user_filename = input("Enter image filename:")
            user_filename = user_filename.lower()

            while not is_valid_image_file(user_filename):
                print ("Invalid image file.")
                user_filename = input("Enter image filename:")

            if is_valid_image_file(user_filename):
                size, image_data = load_image_data(user_filename)
                key, text = get_data_to_encrypt(size)
                encrypted_text = encrypt_text(key, text)
                encrypted_ascii_data = char_to_ascii(encrypted_text)

                key_ascii_data = char_to_ascii(key)
                encrypted_binary_data = ascii_to_binary(encrypted_ascii_data)
                key_binary_data = ascii_to_binary(key_ascii_data)

                modified_image_data = encode_message(image_data, key_binary_data, encrypted_binary_data)
                user_filename = "output/modified_" + os.path.basename(user_filename)
                save_image_to_file(user_filename, size, modified_image_data)


        elif user_input == "decrypt":
            n_user_filename = input("Enter image filename:")
            n_user_filename = n_user_filename.lower()

            while not is_valid_image_file(n_user_filename):
                print ("Invalid image file.")
                n_user_filename = input("Enter image filename:")

            if is_valid_image_file(n_user_filename):
                n_size, n_image_data = load_image_data(n_user_filename)
                binary_key, binary_message = decode_message(n_image_data)
                if decode_message(n_image_data) != (None, None):
                    encrypted_key = binary_to_ascii_string(binary_key)
                    encrypted_message = binary_to_ascii_string(binary_message)
                    if is_valid_message(encrypted_message) and is_valid_key(encrypted_key):
                        n_user_filename = os.path.basename(n_user_filename)
                        n_user_filename = n_user_filename.split(".")
                        n_user_filename =  os.path.join("output", n_user_filename[0] + "_decoded_message.txt")
                        save_file(n_user_filename, decrypt_text(encrypted_message, encrypted_key))

                    else:
                        print ("Error: cannot decode message!")

                else:
                    print ("Error: cannot decode message!")

        user_input = input("Select program mode: (encrypt/decrypt/exit):")

    else:
        print ("Thank you for using this program!")

if __name__ == "__main__":
    main()

