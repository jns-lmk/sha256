from math import floor
import os
import time 

# Wir haben uns zum Teil an diesem Blog Beitrag orientiert.
# https://nickyreinert.medium.com/wie-funktioniert-der-sha256-algorithmus-im-detail-teil-1-2-7a0023cf562a

def clear_console():
    # Überprüfe das Betriebssystem
    if os.name == 'nt':  # Für Windows
        os.system('cls')
    else:  # Für Linux und macOS (os.name == 'posix')
        os.system('clear')

def all_bits(num_bits: int):
    return (1 << num_bits) - 1

def bit_not(n):
    return ~n & all_bits(32)

def choose(x: int, y: int, z: int):
    return ( x & y ) ^ ( ~x & z )

def majority(x: int, y: int, z: int):
    
    return ( x & y ) ^ ( x & z ) ^ ( y & z )
def rot_right(x: int, b: int, bits=32):
    
    return (x >> b) | (x << bits - b)
def cap_sigma_0(x: int):
    return rot_right(x,2) ^ rot_right(x,13) ^ rot_right(x,22)

def cap_sigma_1(x: int):
    return rot_right(x,6) ^ rot_right(x,11) ^ rot_right(x,25)

def sigma_0(x: int):
    return rot_right(x,7) ^ rot_right(x, 18) ^ ( x >> 3 )

def sigma_1(x: int):
    return rot_right(x,17) ^ rot_right(x,19) ^( x >> 10 )

# Die ersten 64 Primzahlen. Diese habe ich aus dem Internet.
first_64_prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]

print("### WILLKOMMEN BEI SHA-256 ####")
print()
# Benutzer zur Eingabe auffordern
message = input("Geben Sie ihren Text einen welcher verschlüsselt werden soll.")
message = message.strip()
# Berechnung der Hash-Werte für IV initialisierung.
compression_constants = []
print("Berechnung von der IV Initialisierungswerten:")
for prime_number in first_64_prime_numbers[0:8]:
    square_root = prime_number ** (1./2.)
    frac_part = square_root - floor(square_root)
    product = frac_part * (2**32)
    floored_product = floor(product)
    print(hex(floored_product))
    time.sleep(0.2)
    compression_constants.append(int(floored_product))

time.sleep(1)
clear_console()

# Berechnung der Hashwerte für die Rundenfunktion
print("Berechnung der Hashwerte für die Rundenfunktion:")
result_constants = []
for prime_number in first_64_prime_numbers:
    cube_root = prime_number ** (1./3.)
    frac_part = cube_root - floor(cube_root)
    product = frac_part * (2**32)
    floored_product = floor(product)
    print(hex(floored_product))
    time.sleep(0.1)
    result_constants.append(int(floored_product))

time.sleep(1)
clear_console()

# Umwandeln der nachricht in numerische Repräsentation
dec_message = []
for char in message:
    dec_message.append(ord(char))
print(f'Numerische Repräsentation der Nachricht: {dec_message}')

# Transformation in Binärsystem um die Länge zu identifizieren
bin_message = ''
for decimal in dec_message:
    bin_message += '0' + bin(decimal)[2:]

len_bin_message = len(bin_message)
print(f'Die Länge deiner Nachricht beträgt {len_bin_message} bits.')
time.sleep(2)
clear_console()

# Die Längenangabe muss exakt 64 Bit belegen. 
# Wir wandeln sie also auch in eine binäre Zahl um hängen vorne 
# Nullen ran um genau 64 Stellen zu erhalten:
rest_to_64 = 64 - len(bin(len_bin_message)[2:])
bin_message_len = '0' * rest_to_64 + bin(len_bin_message)[2:]

# Auf 512 bits bringen = Nachricht + 1 als Trennzeichen
payload = bin_message + '1' + bin_message_len
len_payload = len(payload)
pad_string = int(512 - (len_payload % 512))
full_message = bin_message + '1' + ('0' * pad_string) + bin_message_len
time.sleep(1)
clear_console()

# Das konvertieren der Nachricht von bits in Bytearray
full_message_bytes = bytearray(int(full_message[i:i+8], 2) for i in range(0, len(full_message), 8))

# Ausgabe des `bytearray`
print("Konvertierung von Bit in Bytearray...")
print(f'Vollständige Nachricht in bits: {full_message}')
print(f'Vollständige Nachricht in ByteArray: {full_message_bytes}')
time.sleep(2)
clear_console()

# Erstellung von Blocks für die Nachricht.
blocks = []
for i in range(0, len(bin_message_len), 64): # 64 Bytes sind 512 Bits
    blocks.append(full_message_bytes[i:i+64]) # 64 Bytes / 512 Bits als einzelnen BLock aufnehmen

# Jeden Block separate bearbeiten
for block in blocks:

    # Zwischenspeicher für erweiterten Block initialisieren
    block_exp = []

    # Jeden Block in 64 Teile mit 32 Bit unterteilen
    for t in range(0,64):

        # Die ersten 16 Teile einfach nur anhängen
        if t < 16:
            block_exp.append(bytes(block[t*4:(t*4)+4]))

        # Die restlichen 48 anhand der gegebenen Formel erzeugen
        else:
            # Die einzelnen Werte ermitteln
            wim02 = int.from_bytes(block_exp[t-2] ,'big')
            wim07 = int.from_bytes(block_exp[t-7] ,'big')
            wim15 = int.from_bytes(block_exp[t-15],'big')
            wim16 = int.from_bytes(block_exp[t-16],'big')

            # Den Wert W von i anhand der vorgegebenen Formel berechnen
            wi = sigma_1(wim02) + wim07 + sigma_0(wim15) + wim16

            # Den Wert auf 32 Bit bringen und in Big Endian konvertieren
            exp = int(wi % 2**32).to_bytes(4, 'big')

            # Block anhängen
            block_exp.append(exp)
    assert len(block_exp) == 64

    # Das Arbeitsregister mit den ersten Werten h0-h7 initialisieren
    a = compression_constants[0]
    b = compression_constants[1]
    c = compression_constants[2]
    d = compression_constants[3]
    e = compression_constants[4]
    f = compression_constants[5]
    g = compression_constants[6]
    h = compression_constants[7]

    # Register 64-mal aktualisieren
    for t in range(64):
        # Neue Konstanten
        print(f'Pos 0: {a}')
        print(f'Pos 1: {b}')
        print(f'Pos 2: {c}')
        print(f'Pos 3: {d}')
        print(f'Pos 4: {e}')
        print(f'Pos 5: {f}')
        print(f'Pos 6: {g}')
        print(f'Pos 7: {h}')
        
        kj = result_constants[t]
        wj = int.from_bytes(block_exp[t],'big')

        t1 = (h + cap_sigma_1(e) + choose(e,f,g) + kj + wj ) % 2**32
        t2 = (cap_sigma_0(a) + majority(a,b,c) ) % 2**32

        h = g
        g = f
        f = e
        e = ( d + t1 ) % 2**32
        d = c
        c = b
        b = a
        a = ( t1 + t2 ) % 2**32
        time.sleep(0.5)
        clear_console()

# Den i-ten zwischenzeitlichen Hashwert H(i) ermitteln
updates = [a, b, c, d, e, f, g, h]
# Schleife über die Indizes von 0 bis 7
for i in range(8):
    compression_constants[i] = (updates[i] + compression_constants[i]) % 2**32

# Die 8 Werte müssen nun konkatiniert werden.    
hash_value = b''.join(constant.to_bytes(4, 'big') for constant in compression_constants[:8])


print(f'Dein Hash sieht folgendermaßen aus: {hash_value.hex()}')

print()
import hashlib
# SHA-256 Verschlüsselung eines leeren Strings
hash_object = hashlib.sha256(message.encode())
sha256_hash = hash_object.hexdigest()
print(f'Gegenprüfung mit hashlib: {sha256_hash}')
print()
input("Drücken sie eine Taste um das Programm zu beenden")

