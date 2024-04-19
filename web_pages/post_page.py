import os
import json
from typing import List, Dict

import streamlit as st
from streamlit_chatbox import ChatBox, Markdown

from core.core import corefunc

api = corefunc()
HISTORY_LEN=0

character_map={
    "军人": "soldier",
    "大专学生": "student",
    "农民":"farmer"
}
chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)

def get_messages_history(history_len: int, content_in_expander: bool = False) -> List[Dict]:
    '''
    返回消息历史。
    content_in_expander控制是否返回expander元素中的内容，一般导出的时候可以选上，传入LLM的history不需要
    '''

    def filter(msg):
        content = [x for x in msg["elements"] if x._output_method in ["markdown", "text"]]
        if not content_in_expander:
            content = [x for x in content if not x._in_expander]
        content = [x.content for x in content]

        return {
            "role": msg["role"],
            "content": "\n\n".join(content),
        }

    return chat_box.filter_history(history_len=history_len, filter=filter)

def post_page():
    with st.sidebar:
        character_mode = st.selectbox(
            "请选择人设",
            options=["军人", "大专学生", "农民"],
            key = "character_selected",
        )

    default_text = ""
    
    if 'text' not in st.session_state:
        st.session_state.text = default_text

    txt = st.text_area("帖子：", value=st.session_state.text, key="input_area")
    button_cols = st.columns(12)
    gen_but=button_cols[0].button("生成回复")
    exp1_but=button_cols[1].button("例子1")
    exp2_but=button_cols[2].button("例子2")
    chat_box.output_messages()
    
    if exp1_but:
        st.session_state.text = "台灣地區領導人選舉：候選人辯論舉行，各方熱議未來發展方向。民眾期待聽到更多關於經濟、安全和兩岸關係的政策倡議。#台灣選舉 #政治辯論"
        st.rerun()
    elif exp2_but:
        st.session_state.text = "蛋荒：餐桌上的蛋類價格飆升，引發民眾擔憂。養雞場表示受到飼料成本上漲和雞隻生產週期的影響。政府正在考慮應對措施。#蛋價上漲 #供應短缺"
        st.rerun()

    if gen_but:
        history = get_messages_history(HISTORY_LEN)
        chat_box.reset_history()
        chat_box.ai_say([
                Markdown(f"大模型正在分析任务...", in_expander=True, title="人设", state="running"),
                Markdown(f"执行任务中～", in_expander=True, title="执行结果", state="running"),
            ])
        res=api.character_chat(txt, character_map[character_mode], history)
        text = ""
        for token_res in res:
            try:
                token_choice = token_res.get('choices','')[0]
                finish_reason = token_choice.get('finish_reason')
                if finish_reason == 'stop':
                    break
                text += token_res['choices'][0]['delta']['content']
            except Exception as e:
                print(e)
        
            chat_box.update_msg(text)

        print("text:", text)
        chat_box.update_msg(f"{character_mode}", element_index=0, streaming=False,state="complete")
        chat_box.update_msg(text, element_index=1, streaming=False,state="complete")
            