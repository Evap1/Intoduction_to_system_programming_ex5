
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os

class Cipher:
        def __init__(self, key):
            self.key = key

        def applyBounderies(self, a, key):
            convert = a.isupper
            a = a.upper
            diff = 26
            upper = ord('Z')
            index = (ord(a) + key - upper) % diff + upper
            if convert:
                a = a.lower
            return index

        def encryptOneChar(self, a, key):
            if not a.isalpha:
                return a
            else:
                index = Cipher.applyBounderies(self, a, key)
                return chr(index)


class CaesarCipher(Cipher):
        def __init__(self, key):
            super().__init__(key)
            self.key = key

        def encrypt(self, plaintext: str):
            encrypted = ""
            for i in range(len(plaintext)):
                encrypted += Cipher.encryptOneChar(self, plaintext[i], self.key)
            return encrypted

        def decrypt(self, ciphertext: str):
            self.key *= -1
            decrypted = self.encrypt(ciphertext)
            self.key *= -1
            return decrypted


class VigenereCipher(Cipher):
        def __init__(self, key):
            super().__init__(key)
            self.key = key

        def encrypt(self, plaintext: str):
            encrypted = ""
            for i in range(len(plaintext)):
                iterator_key = i % len(self.key)
                encrypted += Cipher.encryptOneChar(self, plaintext[i], self.key[iterator_key])
            return encrypted

        def decrypt(self, ciphertext: str):
            self.key *= -1
            decrypted = self.encrypt(ciphertext)
            self.key *= -1
            return decrypted


def processDirectory(dir_path: str):
        file_path = os.path.join(dir_path)
        files = os.listdir(dir_path)
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except IOError:
            print("Error: Wrong dir path")
        except KeyError:
            print("Error: Your keys are bad")

        useEncrypt = False
        file_convert_extension = '.enc'
        file_rename_extension = '.txt'
        if data.get['mode'] == 'encrypt':
            useEncrypt = True
            file_convert_extension = '.txt'
            file_rename_extension = '.enc'

        for file in files:
            try:
                file, file_extension = os.path.splitext(file)
                if file_extension == file_convert_extension:
                    with open(file_path, 'r') as f:
                        lines = f.readline()
                        f.close()
                    lines = applyMethod(lines, data['key'], useEncrypt)
                    with open(file_path, 'w') as f:
                        f.writelines(lines + '\n')
                        f.close()
                    if not os.path.exists(file + file_rename_extension):
                        os.rename(file + file_extension, file + file_rename_extension)
            except OSError as e:
                print("Error with file opening or renaming")


def applyMethod(lines, key, useEncrypt=True):
        if useEncrypt:
            if isinstance(key, str):
                cipherMethod = CaesarCipher(key)
                [cipherMethod.encrypt(line) for line in lines]
            elif isinstance(key, list):
                cipherMethod = VigenereCipher(key)
                [cipherMethod.encrypt(line) for line in lines]
        else:
            if isinstance(key, str):
                cipherMethod = CaesarCipher(key)
                [cipherMethod.decrypt(line) for line in lines]
            elif isinstance(key, list):
                cipherMethod = VigenereCipher(key)
                [cipherMethod.decrypt(line) for line in lines]
        return lines