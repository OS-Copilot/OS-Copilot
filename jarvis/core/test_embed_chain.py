# # 导入应用实例
# import os
# from embedchain import App

# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_ORGANIZATION"] = "org-fSyygvftM73W0pK4VjoK395W"
# elon_bot = App()

# # 添加不同的数据源
# elon_bot.add("https://en.wikipedia.org/wiki/Elon_Musk")
# elon_bot.add("https://www.forbes.com/profile/elon-musk")
# # 你还可以添加本地数据源，例如pdf、csv文件等。
# # elon_bot.add("/path/to/file.pdf")

# # 查询你的数据并获得答案
# response = elon_bot.query("埃隆·马斯克今天的净资产是多少？")
# print(response)
# # 答：埃隆·马斯克如今的净资产是2587亿美元。
# from langchain.document_loaders import PDFMinerPDFasHTMLLoader
# loader = PDFMinerPDFasHTMLLoader("tet.pdf")
# data = loader.load()[0]
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(data.page_content,'html.parser')
# content = soup.find_all('div')
# import re
# cur_fs = None
# cur_text = ''
# snippets = []   # first collect all snippets that have the same font size
# for c in content:
#     sp = c.find('span')
#     if not sp:
#         continue
#     st = sp.get('style')
#     if not st:
#         continue
#     fs = re.findall('font-size:(\d+)px',st)
#     if not fs:
#         continue
#     fs = int(fs[0])
#     if not cur_fs:
#         cur_fs = fs
#     if fs == cur_fs:
#         cur_text += c.text
#     else:
#         snippets.append((cur_text,cur_fs))
#         cur_fs = fs
#         cur_text = c.text
# snippets.append((cur_text,cur_fs))
# # Note: The above logic is very straightforward. One can also add more strategies such as removing duplicate snippets (as
# # headers/footers in a PDF appear on multiple pages so if we find duplicatess safe to assume that it is redundant info)
# from langchain.docstore.document import Document
# cur_idx = -1
# semantic_snippets = []
# # Assumption: headings have higher font size than their respective content
# for s in snippets:
#     # if current snippet's font size > previous section's heading => it is a new heading
#     if not semantic_snippets or s[1] > semantic_snippets[cur_idx].metadata['heading_font']:
#         metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
#         metadata.update(data.metadata)
#         semantic_snippets.append(Document(page_content='',metadata=metadata))
#         cur_idx += 1
#         continue
 
#     # if current snippet's font size <= previous section's content => content belongs to the same section (one can also create
#     # a tree like structure for sub sections if needed but that may require some more thinking and may be data specific)
#     if not semantic_snippets[cur_idx].metadata['content_font'] or s[1] <= semantic_snippets[cur_idx].metadata['content_font']:
#         semantic_snippets[cur_idx].page_content += s[0]
#         semantic_snippets[cur_idx].metadata['content_font'] = max(s[1], semantic_snippets[cur_idx].metadata['content_font'])
#         continue
 
#     # if current snippet's font size > previous section's content but less tha previous section's heading than also make a new 
#     # section (e.g. title of a pdf will have the highest font size but we don't want it to subsume all sections)
#     metadata={'heading':s[0], 'content_font': 0, 'heading_font': s[1]}
#     metadata.update(data.metadata)
#     semantic_snippets.append(Document(page_content='',metadata=metadata))
#     cur_idx += 1
# print(semantic_snippets)