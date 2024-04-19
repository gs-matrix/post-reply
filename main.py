import os

import streamlit as st
from streamlit_option_menu import option_menu
from web_pages.reply_page import reply_page
from web_pages.post_page import post_page
if __name__=="__main__":

    st.set_page_config(
        "GS-Demo WebUI",
        initial_sidebar_state="expanded",
        layout="wide",
        menu_items={
            'About': f"""欢迎体验！"""
        }
    )

    pages={
        "对话": {
            "icon": "chat",
            "func": reply_page,
        },
        "帖子回复": {
            "icon": "collection",
            "func": post_page,
        }
    }
    with st.sidebar:
        # st.image(
        #     os.path.join(
        #         "img",
        #         "logo白.svg"
        #     ),
        #     use_column_width=True
        # )
        options=list(pages)
        icons=[x["icon"] for x in pages.values()]

        default_index=0
        selected_page=option_menu("",
            options=options,
            icons=icons,
            default_index=default_index,)
    if selected_page=="帖子回复":
        pages[selected_page]["func"]()
    elif selected_page=="对话":
        pages[selected_page]["func"]()