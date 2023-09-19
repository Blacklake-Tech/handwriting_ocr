import streamlit as st
from baidu import baidu_ocr
from dotenv import load_dotenv
from xfyun import xfyun_ocr

load_dotenv()


def main():
    st.title("手写单据识别")

    api_type = st.radio("API", ("百度智能云表格文字识别", "讯飞云"))
    if api_type == "百度智能云表格文字识别":
        baidu_ocr()
    else:
        xfyun_ocr()


if __name__ == "__main__":
    main()
