from .style import classic,trend,asymmetric,tabmode,hotspot,story
import streamlit as st


layout_types = {
    "經典儀表板": classic,
    "趨勢優先視角": trend,
    "左右非對稱佈局": asymmetric,
    "分頁精簡模式": tabmode,
    "地理熱點視角": hotspot,
    "垂直故事線視角": story,
}


def render_layout(mode, figs, data):
    if mode in layout_types:
        try:
            layout_types[mode].render(figs, data)
        except KeyError:
            st.error(f"Layout '{mode}' 不存在！請檢查 LAYOUT_MAP 設定。")
    else:
        st.error(f"未知的佈局模式: {mode}")  
