
import base64


def encode_prop(value):
    value_bytes = value.encode('ascii')
    encoded_bytes = base64.b64encode(value_bytes)
    encoded_value = encoded_bytes.decode('ascii')
    return encoded_value[::-1]


def decode_prop(value):
    value_bytes = value[::-1].encode('ascii')
    decoded_bytes = base64.b64decode(value_bytes)
    decoded_value = decoded_bytes.decode('ascii')
    return decoded_value


print(encode_prop(''))

