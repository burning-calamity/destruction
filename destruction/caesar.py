class CaesarCipher:
    @staticmethod
    def encrypt(text: str, key: int) -> str:
        key = key % 26
        result = []

        for ch in text:
            if 'a' <= ch <= 'z':
                result.append(chr((ord(ch) - ord('a') + key) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                result.append(chr((ord(ch) - ord('A') + key) % 26 + ord('A')))
            else:
                result.append(ch)

        return ''.join(result)

    @staticmethod
    def decrypt(text: str, key: int) -> str:
        return CaesarCipher.encrypt(text, -key)
caesar = CaesarCipher()
