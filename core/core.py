from llama_cpp import Llama


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
