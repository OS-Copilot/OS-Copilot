import re
import json


# 示例字符串
data = '''

'''

# 找出所有单引号的位置
quote_positions = [pos for pos, char in enumerate(data) if char == "'"]

# 检查是否至少有两个单引号
if len(quote_positions) >= 4:
    # 获取第三个单引号的位置
    start_pos = quote_positions[2]
    # 获取最后一个单引号的位置
    end_pos = quote_positions[-1]
    # 提取所需文本
    extracted_text = data[start_pos+1:end_pos]
else:
    extracted_text = "不足以提取文本"


file_path = ""
with open(file_path,"w",encoding="utf-8") as f2:
    f2.write(extracted_text)

