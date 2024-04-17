import json

# 原始字典
data = {
    '1': {
        '1': b'WebcastLikeMessage',
        '2': 7358403126901657908,
        '3': 7357545811846122277,
        '6': 1,
        '8': {
            '1': b'room_like_common_text',
            '2': b'{0:user} {1:string}',
            '3': {'1': b'#ffffffff', '4': 400},
        }
    }
}

# 将字节串转换为字符串
def bytes_to_str(item):
    if isinstance(item, bytes):
        return item.decode('utf-8')
    elif isinstance(item, dict):
        return {k: bytes_to_str(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [bytes_to_str(i) for i in item]
    else:
        return item

data_str = bytes_to_str(data)

# 将字典转换为JSON字符串
json_str = json.dumps(data_str, ensure_ascii=False, indent=4)

print(json_str)
