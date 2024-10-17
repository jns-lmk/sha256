from math import floor
from IPython.display import clear_output
import time 
def rotate(value, rotations, width=32):
    # thx to https://stackoverflow.com/a/59005609/2360229
    if int(rotations) != abs(int(rotations)):
        rotations = width + int(rotations)
    return (int(value) << (width - (rotations%width)) | (int(value) >> (rotations % width))) & ((1 << width) - 1)
    
def sigma0(word):
    part1 = bin(rotate(int(word, 2), 7, 32))
    part2 = bin(rotate(int(word, 2), 18, 32))
    part3 = bin(int(word, 2) >> 3)
    return bin(int(part1, 2) ^ int(part2, 2) ^ int(part3, 2))[2:].zfill(32)

def sigma1(word):
    part1 = bin(rotate(int(word, 2), 17, 32))
    part2 = bin(rotate(int(word, 2), 19, 32))
    part3 = bin(int(word, 2) >> 10)
    return bin(int(part1, 2) ^ int(part2, 2) ^ int(part3, 2))[2:].zfill(32)

def upper_sigma0(word):
    part1 = bin(rotate(int(word, 2), 2, 32))
    part2 = bin(rotate(int(word, 2), 13, 32))
    part3 = bin(rotate(int(word, 2), 22, 32))
    return bin(int(part1, 2) ^ int(part2, 2) ^ int(part3, 2))[2:].zfill(32)

def upper_sigma1(word):
    part1 = bin(rotate(int(word, 2), 6, 32))
    part2 = bin(rotate(int(word, 2), 11, 32))
    part3 = bin(rotate(int(word, 2), 25, 32))
    return bin(int(part1, 2) ^ int(part2, 2) ^ int(part3, 2))[2:].zfill(32)

def choose(word1, word2, word3):
    bin_word1 = (int(word1, 2))
    bin_word2 = (int(word2, 2))
    bin_word3 = (int(word3, 2))
    return bin((bin_word1 & bin_word2) ^ (~bin_word1 & bin_word3))[2:].zfill(32)

def majority(word1, word2, word3):
    bin_word1 = (int(word1, 2))
    bin_word2 = (int(word2, 2))
    bin_word3 = (int(word3, 2))
    return bin((bin_word1 & bin_word2) ^ (bin_word1 & bin_word3) ^ (bin_word2 & bin_word3))[2:].zfill(32)

first_64_prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]
compression_constants = []
for prime_number in first_64_prime_numbers[0:8]:
    square_root = prime_number ** (1./2.)
    frac_part = square_root - floor(square_root)
    product = frac_part * (2**32)
    floored_product = floor(product)
    compression_constants.append(bin(floored_product)[2:].zfill(32))

print(first_64_prime_numbers[0:8])
    
print(int(compression_constants[0],2))
result_constants = []
for prime_number in first_64_prime_numbers:
    cube_root = prime_number ** (1./3.)
    frac_part = cube_root - floor(cube_root)
    product = frac_part * (2**32)
    floored_product = floor(product)
    result_constants.append(bin(floored_product)[2:].zfill(32))


message = "abc"

dec_message = []
for char in message:
    dec_message.append(ord(char))
    
bin_message ='0'+'0'.join(format(x, 'b') for x in bytearray(message, 'utf-8'))
len_bin_message = len(bin_message)
print(f'The binary representation is {bin_message}')

rest_to_64 = 64 - len(bin(len_bin_message)[2:])
bin_message_len = '0' * rest_to_64 + bin(len_bin_message)[2:]

payload = bin_message + '1' + bin_message_len
len_payload = len(payload)

pad_string = int(512 - (len_payload % 512))
print('Need to add %s zeros to get a multiple of 512 bits' % pad_string)

# Nachricht ist die bin_message + Padding der Nullen + die länge der Nachricht
full_message = bin_message + '1' + ('0' * pad_string) + bin_message_len
print('Check the length: ' + str(len(full_message)) + ' bits')

message_block_length = 512
message_blocks = [full_message[i:i+message_block_length] for i in range(0, len(full_message), message_block_length)]
print('We have %s message blocks' % (len(message_blocks)))


current_hash = compression_constants.copy()

for block in message_blocks:
    message_schedule = []
    for i in range(0,len(block),32):
        message_schedule.append(block[i:i+32])
      
    for i in range(16,64):
        wim02 = message_schedule[i-2] #01010011011101000111001001101001
        wim07 = message_schedule[i-7]
        wim15 = message_schedule[i-15]
        wim16 = message_schedule[i-16]

        new_word = ( \
        int(sigma1(wim02), 2) + \
        int(wim07, 2) + \
        int(sigma0(wim15), 2) + \
        int(wim16, 2)) & \
        int('11111111111111111111111111111111', 2)
        
        #print(bin(new_word)[2:].zfill(32))
        #wi = int(sigma1(wim02),2) + int(wim07,2) + int(sigma0(wim15),2) + int(wim16,2)
        #exp = bin(wi)[2:].zfill(32)
        #print(exp)
        message_schedule.append(bin(new_word)[2:].zfill(32))
    print(len(message_schedule))
    
    next_hash = current_hash.copy()
    print(len(next_hash))
    
    for i, word in enumerate(message_schedule):

        result_constant = result_constants[i]

        term1 = (int(upper_sigma1(next_hash[4]), 2) + \
                int(choose(next_hash[4], next_hash[5], next_hash[6]), 2) + \
                int(next_hash[7], 2) + \
                int(result_constant, 2) + \
                int(word, 2)) \
                & int('11111111111111111111111111111111', 2)
        
        term2 = (int(upper_sigma0(next_hash[0]), 2) + \
                int(majority(next_hash[0], next_hash[1], next_hash[2]), 2)) & int('11111111111111111111111111111111', 2)
        
        # move elements in list one index down, means: last one will be dropped
        # and first one is empty now
        next_hash.insert(0, 1)
        next_hash.pop()

        next_hash[0] = bin(
                (term1 + term2) & int('11111111111111111111111111111111', 2)
            )[2:].zfill(32)

        next_hash[4] = bin(
                (int(next_hash[4], 2) + term1) & int('11111111111111111111111111111111', 2)
            )[2:].zfill(32)
        
        result = []
    # add initial constants to compressed numbers
    for i in range(0, 8):
            result.append(
                    bin(int(current_hash[i], 2) + int(next_hash[i], 2) & int('11111111111111111111111111111111', 2))[2:].zfill(32)
            )

    current_hash = result.copy()

for word in result:
        print(bin(int(word, 2))[2:].zfill(8) + '', end = '')

print()

for word in result:
        print(hex(int(word, 2))[2:].zfill(8) + '', end = '')




#e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
print()
import hashlib
# SHA-256 Verschlüsselung eines leeren Strings
hash_object = hashlib.sha256(message.encode())
sha256_hash = hash_object.hexdigest()

print(sha256_hash)