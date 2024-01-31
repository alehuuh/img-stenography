# Image Stenography

* The program will prompt the user to enter the secret_key and the message to be encrypted in the provided image. Also, it can decrypt the message given the key from image data. It automatically saves decrypted message to text file.
* The program is capable of hiding and finding a short encrypted message inside a given image.

## Program Mode
* If the user enters ‘encrypt’ or ‘decrypt’, the program proceeds with asking the user to type in the filename of the image to be used. If the filename points to a file that either doesn’t exist or isn’t the right format (not a JPEG file: .jpg or ,jpeg), the program shows the message ‘Invalid image file’ and will repeatedly prompt the user to enter a new filename until a valid file is found.
* If the user selects ‘encrypt’ mode, the program will prompt the user to enter the secret_key (‘Enter Key:’) and the message (‘Enter Message:’) to be encrypted.
* If the user selects ‘decrypt’ mode, the program will proceed with processing the image data loaded from the provided filename
* If at any point during the decoding process the program finds that the image cannotbe decoded, the program should show the message ‘Error: cannot decode message!’ and go back to the program menu.

## Constraints
*	secret_key - Contains only ‘u’ or ‘d’ characters. Length should be at least 3 and at most 20 characters.
*	message - Contain characters from the ASCII table with values between 32 and 126. Length should be at least 10 and at most 1000 characters.
* If the above constraints are not met, the program should show the message ‘Invalid Key/Message. Please Try
again.’ and prompt the user to re-enter both secret_key and message, this will repeat until a valid secret_key and
message is entered.
* If the image cannot accommodate the entire secret_key and message, the program should show the message ‘Message and Key cannot fit in the image.’ and prompt the user to re-enter both secret_key and message, this will repeat until a valid secret_key and message is entered. For example, the secret_key ‘udd’ and the message ‘Hello World’, there are a total of 14 characters or 112 bits (14 char * 8 bits/char), so to accommodate the secret_key and message, the image should have at least 6 pixels + (112 bits/(3 bits/pixel)) = 43.33 ≈ 44 pixels (always round up).
