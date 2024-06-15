
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


def sort_dict(dict_list, sort_key, start_idx, end_idx):
    
    if(start_idx<end_idx):
        pivot_ele_idx = start_idx
        i = start_idx
        j = end_idx

        while(i<j):
            
            while(i<end_idx and dict_list[i][sort_key]<=dict_list[pivot_ele_idx][sort_key]):
                i+= 1

            while(j>start_idx and dict_list[pivot_ele_idx][sort_key]<=dict_list[j][sort_key]):
                j-= 1

            if(i<j):

                tmp_dict = dict_list[j]
                dict_list[j] = dict_list[i]
                dict_list[i] = tmp_dict

        tmp_dict = dict_list[j]
        dict_list[j] = dict_list[pivot_ele_idx]
        dict_list[pivot_ele_idx] = tmp_dict

        sort_dict(dict_list, sort_key, start_idx, j-1)
        sort_dict(dict_list, sort_key, j+1, end_idx)


print(encode_prop(''))

