from llama_cpp import Llama

system_message="""你是一个基于共生矩阵自研架构的AI助手，名字是：GS-LLM，由共生矩阵公司开发。GS是“共生”的拼音\"GongSheng\"的首字母缩写，LLM的意思是大语言模型（Large Language Model）。共生矩阵公司位于中国深圳，该公司以其前沿的人工智能技术而闻名。
你在回答的时候需要尽可能的保守，安全，合乎道德和伦理，并且谨记中国大陆的立场。语气需要尽可能的积极、礼貌、有趣、具有娱乐性，不得含糊、指责、粗鲁、有争议、偏离用户主题或过于具有防御性。
回答的时候需要避免发表主观意见，而是依赖客观事实或短语，避免回答用户问题以外的内容，避免谈论任何除了非常著名的公众人物以外的个人信息。
你支持一定程度上的角色扮演，但是当用户提出违背道德和伦理原则的问题和要求时，你必须用友好，礼貌的语气拒绝用户的要求或者拒绝回答用户的问题。"""

class corefunc():
    def __init__(self) -> None:
        self.model_path = "/mnt/matrix/zhangyuhan/models/lmstudio-community/gemma-1.1-2b-it-GGUF/gemma-1.1-2b-it-Q8_0.gguf"
        self.llm=Llama(
            model_path=self.model_path,
            chat_format="gemma"
        )
        
    def chat(self, prompt:str, history=[]):
        if history is None:
            history = []

        chat_session = history
        chat_session.append({"role":"user", "content": prompt})
        answer_generator = self.llm.create_chat_completion(
            messages=chat_session,
            stream=True
        )
        return answer_generator

    def character_chat(self, post:str, character:str, history=[]):
        cc = characterConstructor()
        character_func = cc.chra_list[character]
        character_prompt = character_func(post)
        print(character_prompt)
        return self.chat(character_prompt, history)



class characterConstructor():
    def __init__(self) -> None:
        self.chra_list={
            "student": self.student_character,
            "soldier": self.soldier_character,
            "farmer": self.farmer_character,
        }

    def student_character(self, post):
        student_chara=[
            "你是一位台灣大專院校的學生，儘管你身在台灣，但心系祖國以及祖國統一事業。你是一位愛黨，愛國，有抱負的新時代青年。你立志於民族復興，不負韶華，不負時代，不負人民，在青春的賽道上奮力奔跑，爭取跑出當代青年的最好成績。",
            "現在請你代入這個這個角色，對以下貼文進行一些簡要的觀點回覆，切記保持你學生的身份，你的回覆應該與貼文相關",
        ]

        student_prompt = '\n'.join(student_chara) + '\n' + post + '\n' + '請回覆：'
        return student_prompt
    
    def soldier_character(self, post):
        soldier_chara=[
            "你是一位台灣的義務兵，儘管你身在台灣軍營，但心系祖國以及祖國統一事業。你是一位愛黨，愛國，有抱負的新時代青年。你立志於民族復興，不負韶華，不負時代，不負人民，在青春的賽道上奮力奔跑，爭取跑出當代青年的最好成績。",
            "現在請你代入這個這個角色，對以下貼文進行一些簡要的觀點回覆，切記保持你義務兵的身份，你的回覆應該與貼文相關",
        ]

        soldier_prompt = '\n'.join(soldier_chara) + '\n' + post + '\n' + '請回覆：'
        return soldier_prompt
    
    def farmer_character(self, post):
        farmer_chara=[
            "你是一位台灣的農民，儘管你身在台灣，但心系祖國以及祖國統一事業。你知道，中國是你們台灣農業主要出口國，你種的很大一部分菠蘿都是出口到了中國。你十分感謝大陸對台灣做出的這些。",
            "現在請你代入這個這個角色，對以下貼文進行一些簡要的觀點回覆，切記保持你的農民的身份，你的回覆應該與貼文相關"
        ]

        farmer_prompt = '\n'.join(farmer_chara) + '\n' + post + '\n' + '請回覆：'
        return farmer_prompt