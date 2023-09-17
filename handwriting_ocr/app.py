import base64
import hashlib
import json
import os
import time
from typing import Optional, TypedDict

import streamlit as st
from dotenv import load_dotenv

from handwriting_ocr.xfyun import xfyun_ocr

load_dotenv()


def main():
    st.title("手写单据识别")

    xfyun_ocr()


if __name__ == "__main__":
    main()
