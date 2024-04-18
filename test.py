from llama_cpp import Llama
import numpy as np
llm = Llama(
        model_path="/mnt/matrix/zhangyuhan/models/lmstudio-community/gemma-1.1-2b-it-GGUF/gemma-1.1-2b-it-Q8_0.gguf",
        chat_format="gemma"
    )

generator = llm.create_chat_completion(
      messages = [
            {
                "role": "system", 
                "content": "You are an assistant who perfectly describes images."
            },
            {
                "role": "user",
                "content": "Describe this image in detail please."
            }
      ],
      stream=True,
)

for y in generator:
    print(y)

#generator
# def stop_criteria(inputid, logits):
#     return np.argmax(logits) == 2

# query = "中國的四大名著有什麽？".encode("utf-8")
# tokens = llm.tokenize(text = bytes(query))

# for token in llm.generate(
#     tokens, 
#     top_k=40, 
#     top_p=0.95, 
#     temp=1.0, 
#     repeat_penalty=1.1,
#     stopping_criteria=stop_criteria):
    
#     print(llm.detokenize([token]).decode("utf-8"))

# output = llm(
#       "中國的四大名著有什麽？", # Prompt
#       max_tokens=None, # Generate up to 32 tokens, set to None to generate up to the end of the context window
#       stop=["</s>"], # Stop generating just before the model would generate a new question
#       echo=True # Echo the prompt back in the output
# ) 
# print(output)