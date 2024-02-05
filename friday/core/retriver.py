from openai import OpenAI
from utils import cosine_similarity
import json

"""
    Use to generate embedding of the text
"""
class OpenAIEmbeddingAndRetriver:
    """
      OPEN AI Chat Models
    """
    def __init__(self, config_path=None):
        with open(config_path) as f:
            config = json.load(f)
        self.model_name = "text-embedding-ada-002"
        self.client = OpenAI(api_key=config['OPENAI_API_KEY'], organization=config['OPENAI_ORGANIZATION'])
        
    # get the embedding of a text
    def get_text_embedding(self,text):
        texts_embeddings = self.client.embeddings.create(
        model= self.model_name,
        input=[text])
        return texts_embeddings.data[0].embedding
    # get the embeddings of each text in the list
    def get_texts_embedding(self,text_list):
        texts_embeddings = self.client.embeddings.create(
        model= self.model_name,
        input=text_list)
        return [obj.embedding for obj in texts_embeddings.data]

    # retrive the most similar text with query in the text_list
    def retrive(self,query,text_list,top_k=1):
        texts_embeddings = self.get_texts_embedding(text_list)
        query_embedding = self.get_text_embedding(query)
        similarity = []
        for emb in texts_embeddings:
            similarity.append(cosine_similarity(emb ,query_embedding))
        sorted_pairs=sorted(zip(similarity, text_list), reverse=True)
        retrieved_texts = [pair[1] for pair in sorted_pairs]
        return retrieved_texts[:top_k]

# embed = OpenAIEmbeddingAndRetriver("../../examples/config.json")
# res = embed.retrive("set a 10s timer",["resume screen","set_timer","print_words","get_timer"])
# print(res)



