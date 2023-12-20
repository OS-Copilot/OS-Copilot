# 导入应用实例
import os
from embedchain import App

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_ORGANIZATION"] = "org-fSyygvftM73W0pK4VjoK395W"
elon_bot = App()

# 添加不同的数据源
elon_bot.add("https://en.wikipedia.org/wiki/Elon_Musk")
elon_bot.add("https://www.forbes.com/profile/elon-musk")
# 你还可以添加本地数据源，例如pdf、csv文件等。
# elon_bot.add("/path/to/file.pdf")

# 查询你的数据并获得答案
response = elon_bot.query("埃隆·马斯克今天的净资产是多少？")
print(response)
# 答：埃隆·马斯克如今的净资产是2587亿美元。