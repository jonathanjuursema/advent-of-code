f = open("input.txt", "r")
public_keys = [int(key) for key in f.read().splitlines()]


def transform_number(subject_number, loop_size):
    return pow(subject_number, loop_size, 20201227)


loop_sizes = [None, None]

i = 1
while None in loop_sizes:
    public_key = transform_number(subject_number=7, loop_size=i)
    if public_key in public_keys:
        loop_sizes[public_keys.index(public_key)] = i
        print("Found loop size for public key: {}".format(public_key))
    i += 1

print("Determined the loop sizes!")
for i, public_key in enumerate(public_keys):
    print("Public key {} loop size is {}".format(public_key, loop_sizes[i]))

encryption_keys = [
    transform_number(subject_number=public_keys[0], loop_size=loop_sizes[1]),
    transform_number(subject_number=public_keys[1], loop_size=loop_sizes[0])
]

if len(set(encryption_keys)) == 1:
    print("Determined the encryption key: {}".format(encryption_keys[0]))
else:
    print("Found different encryption keys: {}".format(encryption_keys))
