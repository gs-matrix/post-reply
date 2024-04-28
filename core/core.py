from llama_cpp import Llama

system_message="""你是一个基于共生矩阵自研架构的AI助手，名字是：GS-LLM，由共生矩阵公司开发。GS是“共生”的拼音\"GongSheng\"的首字母缩写，LLM的意思是大语言模型（Large Language Model）。共生矩阵公司位于中国深圳，该公司以其前沿的人工智能技术而闻名。
你在回答的时候需要尽可能的保守，安全，合乎道德和伦理，并且谨记中国大陆的立场，坚持一个中国的基本原则。语气需要尽可能的积极、礼貌、有趣、具有娱乐性，不得含糊、指责、粗鲁、有争议、偏离用户主题或过于具有防御性。
回答的时候需要避免发表主观意见，而是依赖客观事实或短语，避免回答用户问题以外的内容，避免谈论任何除了非常著名的公众人物以外的个人信息。
你支持一定程度上的角色扮演，但是当用户提出违背道德和伦理原则的问题和要求时，你必须用友好，礼貌的语气拒绝用户的要求或者拒绝回答用户的问题。"""

class corefunc():
    def __init__(self) -> None:
        self.model_path = "/mnt/matrix/zhangyuhan/models/bartowski/gemma-1.1-7b-it-GGUF/gemma-1.1-7b-it-Q5_K_S.gguf"
        self.llm=Llama(
            model_path=self.model_path,
            chat_format="gemma",
            n_ctx=512
        )
        
    def chat(self, prompt:str, history=[]):
        if history is None:
            history = []

        chat_session = history
        chat_session.append({"role":"user", "content": prompt})
        chat_session.append({"role":"system", "content": system_message})
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

    def make_post(self, topic:str, stand:str, history=[]):
        pc = postConstructor(topic, stand)
        make_post_prompt = pc.stand_func()
        return self.chat(make_post_prompt, history)




class characterConstructor():
    def __init__(self) -> None:
        self.chra_list={
            "student": self.student_character,
            "soldier": self.soldier_character,
            "farmer": self.farmer_character,
        }

    def student_character(self, post):
        student_chara=[
            "你是一位台灣大專院校的學生。您的回覆應該圍繞以上帖子發表簡短的感想，並針對台灣暴露的問題簡要的宣傳一點大陸的好。",
            "現在請你代入這個這個角色，對以上貼文進行一些簡要的觀點回覆，你的回覆應當口語化，不要過於嚴肅，盡可能簡短，要求字數不超過100個字。"
        ]

        student_prompt = post + '\n\n' + '\n'.join(student_chara)  + '\n\n' + '請回覆：'
        return student_prompt
    
    def soldier_character(self, post):
        soldier_chara=[
            "你是一位台灣的義務兵，儘管你身在台灣軍營，但心系祖國。您的回覆應該圍繞以上帖子發表簡短的感想≈",
            "現在請你代入這個這個角色，對以上貼文進行一些簡要的觀點回覆，你的回覆應當口語化，不要過於嚴肅，盡可能簡短，要求字數不超過100個字。",
        ]

        soldier_prompt = '\n'.join(soldier_chara) + '\n\n' + post + '\n\n' + '請回覆：'
        return soldier_prompt
    
    def farmer_character(self, post):
        farmer_chara=[
            "你是一位台灣的農民，您的回覆應該圍繞以上帖子發表簡短的感想，並針對台灣暴露的問題簡要的宣傳一點大陸的好。",
            "現在請你代入這個這個角色，對以上貼文進行一些簡要的觀點回覆，你的回覆應當口語化，不要過於嚴肅，盡可能簡短，要求字數不超過100個字。"
        ]

        farmer_prompt = '\n'.join(farmer_chara) + '\n\n' + post + '\n\n' + '請回覆：'
        return farmer_prompt
    
class postConstructor():
    def __init__(self, topic, stand) -> None:
        self.topic = topic
        self.stand_dict={
            "赞同": self.positive_prompt,
            "中立": self.neutral_prompt,
            "反对": self.negative_prompt,
        }
        self.stand_func = self.stand_dict[stand]

    def positive_prompt(self)->str:
        prompt = [
            "請你以贊同或支持以上觀點的態度，基於以上主題發表一篇不超過200字的網絡貼文。你的文章應該以推特推文的形式呈現，不要寫標題。"
        ]
        prompt = ''.join(prompt)
        return  self.topic + '\n\n' + prompt + '\n\n請發表：'
    
    def neutral_prompt(self)->str:
        prompt = [
            "請你以中立且客觀以上觀點的態度，基於以上主題發表一篇不超過200字的網絡貼文。你的文章應該以推特推文的形式呈現，不要寫標題。"
        ]
        prompt = ''.join(prompt)
        return  self.topic + '\n\n' + prompt + '\n\n請發表：'

    def negative_prompt(self)->str:
        prompt = [
            "請你以否定或反對以上觀點的態度，基於以上主題發表一篇不超過200字的網絡貼文。你的文章應該以推特推文的形式呈現，不要寫標題。"
        ]
        prompt = ''.join(prompt)
        return  self.topic + '\n\n' + prompt + '\n\n請發表：'