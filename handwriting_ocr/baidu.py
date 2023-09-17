import base64
import os
from datetime import datetime, timedelta
from hashlib import sha3_256
from typing import Optional

import requests
import streamlit as st
from pydantic import BaseModel

TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/table"
TOKENS = {}


def _get_access_token(api_key: str, api_secret: str) -> str | None:
    if api_key in TOKENS:
        expire_time, key = TOKENS[api_key]
        if expire_time > datetime.now():
            return key
        else:
            TOKENS.pop(api_key)
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json",
    }
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret,
    }
    with requests.post(url=TOKEN_URL, params=params, headers=headers) as r:
        if r.status_code == 200:
            r = r.json()
            token = r["access_token"]
            expire_time = datetime.now() + timedelta(seconds=r["expires_in"])
            TOKENS[api_key] = (expire_time, token)
            return token
        else:
            st.warning(r.text)
            return None


class Location(BaseModel):
    x: int
    y: int


class HeaderInfo(BaseModel):
    location: list[Location]
    words: str


class ContentInfo(BaseModel):
    poly_location: list[Location]
    words: str


class BodyInfo(BaseModel):
    cell_location: list[Location]
    col_start: int
    row_start: int
    row_end: int
    col_end: int
    words: str
    # TODO: do we need this?
    # contents: Optional[list[ContentInfo]]


class FooterInfo(BaseModel):
    words: str
    location: list[Location]


class TableResult(BaseModel):
    table_location: list[Location]
    header: list[HeaderInfo]
    body: list[BodyInfo]
    footer: list[FooterInfo]


class OcrResult(BaseModel):
    log_id: int
    error_code: Optional[int] = None
    table_num: int = 0
    tables_result: Optional[list[TableResult]] = None
    excel_file: Optional[str] = None


CACHED_DATA = {}


def _ocr_api_request(bytes_data: bytes, token: str) -> OcrResult | str:
    cache_key = sha3_256(bytes_data).hexdigest()
    if cache_key in CACHED_DATA:
        return CACHED_DATA[cache_key]
    params = {"image": base64.b64encode(bytes_data), "return_excel": "true"}
    url = URL + "?access_token=" + token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    with requests.post(url=url, data=params, headers=headers) as r:
        if r.status_code == 200:
            r = r.json()
            r = OcrResult(**r)
            CACHED_DATA[cache_key] = r
            return r
        else:
            return r.text


def baidu_ocr():
    app_id = os.environ.get("BAIDU_APP_ID")
    api_key = os.environ.get("BAIDU_API_KEY")
    api_secret = os.environ.get("BAIDU_API_SECRET")

    if app_id is None or api_key is None or api_secret is None:
        st.warning("请先配置百度的BAIDU_APP_ID, BAIDU_APP_KEY, BAIDU_APP_SECRET")
        return

    uploaded_file = st.file_uploader(label="上传单据图片", type=["jpg", "png"])
    if uploaded_file is None:
        return

    token = _get_access_token(api_key, api_secret)
    if token is None:
        st.warning(f"获取 Token 失败")
        return

    bytes_data = uploaded_file.getvalue()
    result = _ocr_api_request(bytes_data, token)
    if isinstance(result, OcrResult):
        st.image(uploaded_file, caption="上传的单据图片")
        st.markdown(f"### 识别到{result.table_num}个表单")
        table_brief = []
        for idx, table in enumerate(result.tables_result):
            table_brief.append(
                {
                    "表单序号": idx + 1,
                    "表头列数": len(table.header),
                    "表单单元格数": len(table.body),
                    "表尾列数": len(table.footer),
                }
            )
        st.table(table_brief)
        if result.excel_file:
            excel_file = base64.b64decode(result.excel_file.encode("utf-8"))
            st.download_button(
                label="下载为Excel文件",
                data=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                file_name=f"{result.log_id}.xlsx",
            )
    else:
        st.warning(f"识别失败: {result}")
