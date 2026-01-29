class VigenereCipher:
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        if not key or not key.isalpha():
            raise ValueError("Key must be a non-empty alphabetic string")

        result = []
        key = key.lower()
        key_len = len(key)
        key_index = 0

        for ch in text:
            if ch.isalpha():
                shift = ord(key[key_index % key_len]) - ord('a')
                if ch.islower():
                    result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(ch)

        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        if not key or not key.isalpha():
            raise ValueError("Key must be a non-empty alphabetic string")

        result = []
        key = key.lower()
        key_len = len(key)
        key_index = 0

        for ch in text:
            if ch.isalpha():
                shift = ord(key[key_index % key_len]) - ord('a')
                if ch.islower():
                    result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(ch)

        return ''.join(result)

vigenere = VigenereCipher()
