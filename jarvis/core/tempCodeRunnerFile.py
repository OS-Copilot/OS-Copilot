text = re.sub(r'\s+', ' ', text )
# 去除空行
text = re.sub(r'\n\s*\n', '\n', text)