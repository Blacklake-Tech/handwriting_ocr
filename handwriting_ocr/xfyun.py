import base64
import hashlib
import json
import os
import time
from typing import Optional

import requests
import streamlit as st
from pydantic import BaseModel

URL: str = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"


def xfyun_ocr():
    app_id: str = os.environ.get("XF_APP_ID")
    app_key: str = os.environ.get("XF_APP_KEY")

    if app_id is None or app_key is None:
        st.warning("请先配置讯飞的XF_APP_ID和XF_APP_KEY")
        return

    lang_type = st.radio("语言类型", ["只有英文", "中英混合"], index=1)
    if lang_type == "只有英文":
        language = "en"
    else:
        language = "cn|en"

    uploaded_file = st.file_uploader(label="上传单据图片", type=["jpg", "png"])
    if uploaded_file is None:
        return

    header = _get_xfyun_request_header(
        language, location="true", app_id=app_id, app_key=app_key
    )

    bytes_data = uploaded_file.getvalue()
    b64_encoded_str = str(base64.b64encode(bytes_data), "utf-8")
    body = {"image": b64_encoded_str}
    with requests.post(url=URL, headers=header, data=body) as r:
        if r.status_code == 200:
            st.image(uploaded_file, caption="上传的单据图片")
            result = r.json()
            result: OcrResult = OcrResult(**result)
            # for each block, present a table using st.table, and in each table, for its block,
            # for each line, present three columns: location XxY, words in an array, and confidence
            for idx, block in enumerate(result.data.block):
                st.write(f"Block #{idx + 1}, 一共{len(block.line)}行")
                line_data = []
                for line in block.line:
                    line_data.append(
                        {
                            "图片中位置": f"[{line.location.top_left.x}, {line.location.top_left.y}]",
                            "文字": ", ".join([word.content for word in line.word]),
                            "置信度": line.confidence,
                        }
                    )
                st.table(line_data)
        else:
            st.warning(f"识别失败: {r.text}")


def _get_xfyun_request_header(
    language: str,
    location: str,
    app_id: str,
    app_key: str,
) -> dict[str, str]:
    """
    获取讯飞请求头
    """
    cur_time = str(int(time.time()))
    param = json.dumps({"language": language, "location": location})
    param_base64 = base64.b64encode(param.encode("utf-8"))
    m2 = hashlib.md5()
    str1 = app_key + cur_time + str(param_base64, "utf-8")
    m2.update(str1.encode("utf-8"))
    checkSum = m2.hexdigest()
    header = {
        "X-CurTime": cur_time,
        "X-Param": param_base64,
        "X-Appid": app_id,
        "X-CheckSum": checkSum,
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }
    return header


class OcrWordInfo(BaseModel):
    content: str


class PointInfo(BaseModel):
    x: int
    y: int


class LocationInfo(BaseModel):
    top_left: PointInfo
    right_bottom: PointInfo


class OcrLineInfo(BaseModel):
    word: list[OcrWordInfo]
    location: Optional[LocationInfo] = None
    confidence: float


class OcrBlockInfo(BaseModel):
    type: str
    line: list[OcrLineInfo]


class OcrData(BaseModel):
    block: list[OcrBlockInfo]


class OcrResult(BaseModel):
    code: str
    data: OcrData
    desc: str
    sid: str
