import os
import hmac
import hashlib

class SecurePRNG:
    def __init__(self, seed=None):
        # Si no se proporciona una semilla, se genera una desde el sistema operativo
        self.seed = seed or os.urandom(32)  # 256 bits de entropía
        self.state = self.seed  # Estado inicial

    def _hash(self, data):
        # Utiliza HMAC-SHA256 para mezclar datos
        return hmac.new(self.state, data, hashlib.sha256).digest()

    def random_bytes(self, length):
        # Genera `length` bytes aleatorios
        result = b""
        while len(result) < length:
            # Mezcla el estado con un contador incremental
            self.state = self._hash(self.state + os.urandom(16))  # Actualiza el estado
            result += self.state
        return result[:length]

    def random_int(self, a, b):
        # Genera un número entero aleatorio entre `a` y `b`
        n = int.from_bytes(self.random_bytes(8), 'big')  # 64 bits
        return a + n % (b - a + 1)


# Instancia del PRNG
prng = SecurePRNG()

# Generar un archivo binario con números aleatorios
with open("secuencia.bin", "wb") as f:
    for _ in range(100000):  # Generar 100,000 números aleatorios
        f.write(prng.random_bytes(4))  # Escribe 4 bytes por número (32 bits)

print("Archivo 'secuencia.bin' generado con éxito.")