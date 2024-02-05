from jarvis.action.get_os_version import get_os_version, check_os_version
from jarvis.core.llms import OpenAI



_FORMAT_SYSTEM_PROMPT = '''
You need to convert the following text to the format described in the format description.
'''
_FORMAT_USER_PROMPT = '''
** Text **
{text}
** Format Description **
{format_description}
** Text After Conversion **
'''



class FormatAgent():
    """
    SkillCreator is used to generate new skills and store them in the action_lib.
    """
    def __init__(self, config_path=None) -> None:
        super().__init__()
        self.llm = OpenAI(config_path)
        self.model_name = self.llm.model_name
        self.system_version = get_os_version()
        try:
            check_os_version(self.system_version)
        except ValueError as e:
            print(e)
        # self.mac_systom_prompts = 

    def convert_format(self, text,format_description):
        self.sys_prompt = _FORMAT_SYSTEM_PROMPT
        self.user_prompt = _FORMAT_USER_PROMPT.format(
            text=text,
            format_description=format_description
        
        )
        self.message = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": self.user_prompt},
        ]
        res = self.llm.chat(self.message)
        print(res)
        return res


text = '''
Zhiyong Wu Research Scientist Shanghai AI Laboratory Email: a@b, a=whucs2013wzy b=gmail.com] [Github] [Google Scholar] About me Hi! I am a research scientist at Shanghai AI Lab. I got my PhD degree from the University of Hong Kong at the end of 2021, affiliated with the HKU database group and NLP group. I am advised by Prof. Ben Kao. I am also working closely with Dr. Lingpeng Kong. Before that, I received my B.E. degree from the Dept. of Computer Science at Wuhan University in 2017. Throughout my graduate studies, I had great internships in Tencent AI Lab and Huawei Noah's Ark Lab. Hiring We have multiple full-time/internship positions available (focus on language agent and multilingual LLM), please feel free to hit me up with your CV or questions if interested. Research I am boardly interested in different topics in NLP. But at the moment, my research focus on exploring interesting (sometimes surprising) utilities of large language models: To synthesis datasets without human annotation. (ZeroGen, ProGen, SunGen) To explain model decision via natural language generation. (Neon, EIB) To learn a task without training by conditioning on in-context examples. (SAIL, CEIL, EvaLM, survey, OpenICL) I'm currently obsessed with the idea of \"LLM-powered autonomous agents\" and have multiple related projects underway. If you are also interested in this topic and have a plan to do an internship, feel free to hit me up via email. Research output of my interns Publications (*: equal contribution) Preprints In-Context Learning with Many Demonstration Examples Mukai Li, Shansan Gong, Jiangtao Feng, Yiheng Xu, Jun Zhang, Zhiyong Wu, Lingpeng Kong. [pdf]. A Survey on In-context Learning Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Zhiyong Wu, Baobao Chang, Xu Sun, Jingjing Xu, Lei Li, Zhifang Sui [pdf]. Corex: Pushing the Boundaries of Complex Reasoning through Multi-Model Collaboration Qiushi Sun, Zhangyue Yin, Xiang Li, Zhiyong Wu, Xipeng Qiu, Lingpeng Kong [pdf]. EMO: Earth Mover Distance Optimization for Auto-Regressive Language Modeling Siyu Ren, Zhiyong Wu, Kenny Q Zhu [pdf]. 2023 Can We Edit Factual Knowledge by In-Context Learning? Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, Baobao Chang EMNLP 2023, Singapore, [pdf]. [code] DiffuSeq-v2: Bridging Discrete and Continuous Text Spaces for Accelerated Seq2Seq Diffusion Models Shansan Gong, Mukai Li, Jiangtao Feng, Zhiyong Wu, Lingpeng Kong. EMNLP 2023, Findings, Singapore, [pdf]. [code] Self-adaptive In-context Learning Zhiyong Wu*, Yaoxiang Wang*, Jiacheng Ye*, Lingpeng Kong. ACL 2023, Toronto, [pdf]. [code] OpenICL: An Open-Source Framework for In-context Learning Zhenyu Wu*, YaoXiang Wang*, Jiacheng Ye*, Jiangtao Feng, Jingjing Xu, Yu Qiao, Zhiyong Wu. ACL 2023, Toronto, Demo paper, [pdf]. [code] Explanation Regeneration via Information Bottleneck Qintong Li, Zhiyong Wu, Lingpeng Kong, Wei Bi. ACL 2023 Findings, Toronto, [pdf]. Compositional Exemplars for In-context Learning Jiacheng Ye, Zhiyong Wu, Jiangtao Feng, Tao Yu, Lingpeng Kong. ICML 2023, Hawaii, [pdf]. [code] DiffuSeq: Sequence to Sequence Text Generation with Diffusion Models Shansan Gong, Mukai Li, Jiangtao Feng, Zhiyong Wu, Lingpeng Kong. ICLR 2023, Rwanda, [pdf]. [code] Self-Guided High-Quality Data Generation in Efficient Zero-Shot Learning Jiahui Gao, Renjie Pi, Yong Lin, Hang Xu, Jiacheng Ye, Zhiyong Wu, Xiaodan Liang, Zhenguo Li, Lingpeng Kong. ICLR 2023, Rwanda, [pdf]. Unsupervised Explanation Generation via Correct Instantiations Sijie Chen, Zhiyong Wu, Jiangjie Chen, Zhixing Li, Yang Liu, and Lingpeng Kong AAAI 2023, Washington, [pdf]. [code] 2022 ProGen: Progressive Zero-shot Dataset Generation via In-context Feedback Jiacheng Ye, Jiahui Gao, Zhiyong Wu, Jiangtao Feng, Tao Yu, and Lingpeng Kong. EMNLP-Findings 2022, long paper.[pdf]. ZeroGen: Efficient Zero-shot Learning via Dataset Generation Jiacheng Ye*, Jiahui Gao*, Qintong Li, Hang Xu, Jiangtao Feng, Zhiyong Wu, Tao Yu and Lingpeng Kong. EMNLP 2022, long paper. [pdf]. [code] Lexical Knowledge Internalization for Neural Conversational Models Zhiyong Wu, Wei Bi, Xiang Li, Lingpeng Kong, Ben Kao. ACL 2022, long paper. [pdf]. [code] COLO: A Contrastive Learning based Re-ranking Framework for One-Stage Summarization Chenxin An, Ming Zhong, Zhiyong Wu, Qin Zhu, Xuanjing Huang, Xipeng Qiu. COLING 2022, long paper. [pdf]. [code] 2021 Good for Misconceived Reasons: An Empirical Revisiting on the Need for Visual Context in Multimodal Machine Translation Zhiyong Wu, Lingpeng Kong, Wei Bi, Xiang Li, Ben Kao. ACL 2021, long paper. [pdf] [code] Cascaded Head-colliding Attention Lin Zheng, Zhiyong Wu, Lingpeng Kong. ACL 2021, long paper. [pdf] [code] 2020 and before Perturbed Masking: Parameter-free Probing for Analyzing and Interpreting BERT Zhiyong Wu, Yun Chen, Ben Kao, Qun Liu. ACL 2020. [pdf] [code] PERQ: Predicting, Explaining, and Rectifying Failed Questions in KB-QA Systems Zhiyong Wu, Ben Kao, Tien-Hsuan Wu, Pengcheng Yin, Qun Liu. WSDM 2020, long paper. [pdf] Towards Practical Open Knowledge Base Canonicalization TTien-Hsuan Wu, Zhiyong Wu, Ben Kao, Pengcheng Yin. CIKM 2018. [pdf] Interns Jiacheng Ye EMNLP'22a, EMNLP'22b, ICML'23 Sijie Cheng AAAI'23 Yaoxiang Wang ACL'23a, ACL'23b Zhenyu Wu ACL'23b Siyu Ren Under review at ICLR'24 Qiushi Sun Under review at ICLR'24 Fangzhi Xu TBA Kanzhi Cheng TBA Yi Lu TBA
'''
format_description = '''
Convert the text into Markdown Format, make it look like a personal blog
'''
agent = FormatAgent("../../examples/config.json")
print(agent.model_name)
res = agent.convert_format(text,format_description)
with open("test.txt","w") as f:
    f.write(res)