import os
import json
from typing import List, Dict

import streamlit as st
from streamlit_chatbox import ChatBox, Markdown

from core.core import corefunc

api = corefunc()
HISTORY_LEN=0

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

def make_post_page():
    with st.sidebar:
        character_mode = st.selectbox(
            "请选择立场",
            options=["赞同", "中立", "反对"],
            key = "character_selected",
        )

    default_text = ""
    
    if 'text' not in st.session_state:
        st.session_state.text = default_text

    txt = st.text_area("主题：", value=st.session_state.text, key="input_area")
    button_cols = st.columns(18)
    gen_but=button_cols[0].button("生成帖子")
    exp1_but=button_cols[1].button("例子1")
    exp2_but=button_cols[2].button("例子2")
    # exp3_but=button_cols[3].button("例子3")
    chat_box.output_messages()
    
    if exp1_but:
        st.session_state.text = "美國國會眾議院4月20日表決通過了價值950億美元的法案，對烏克蘭、以色列及台灣提供軍事援助，該法案即將在參議院獲得通過。"
        st.rerun()
    elif exp2_but:
        st.session_state.text = "以色列在加薩的軍事行動，持續引發美國大學校園的示威浪潮。洛杉磯的南加州大學（USC）以安全為由，取消原定於5月10日舉行的一場主畢業禮。除了南加州大學，美國多地的大學也持續有示威。最近一波校園示威始於哥倫比亞大學管理層讓警察進入校內清場，導致過百人被捕。示威者呼籲各大學“從種族滅絕（行為）中撤資”，停止將學校的大筆捐款投資於參與武器製造的公司，以及其它支持以色列加薩戰爭的行業。"
        st.rerun()

    if gen_but:
        history = get_messages_history(HISTORY_LEN)
        chat_box.reset_history()
        chat_box.ai_say([
                Markdown(f"大模型正在分析任务...", in_expander=True, title="立场", state="running"),
                Markdown(f"执行任务中～", in_expander=False, title="执行结果", state="running"),
            ])
        res=api.make_post(txt, character_mode, history)
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
            