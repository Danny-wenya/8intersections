import json

# 读取未格式化的JSON文件
with open('./SH2/roadnet.json', 'r') as file:
    data = json.load(file)

# 将数据格式化为带缩进的JSON字符串
formatted_json = json.dumps(data, indent=2)

# 将格式化后的JSON写入文件
with open('./SH2/roadnet.json', 'w') as file:
    file.write(formatted_json)
