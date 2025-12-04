from dataquery.repository import ExceedRepository
from datapipeline.feature_engineer import casecount
from datapipeline.charts import (politicalarea_chart,
                                 sunrisehour_chart,
                                 sunrisehourday_chart,
                                 overstandardcount_chart,
                                 carsnorepeatcount_chart)
from layouts.ui import render_sidebar
from layouts    import render_layout
from  db  import  linkdb
import streamlit as st
import pandas as pd


#-- 頁面設定與配置 --# 
st.set_page_config(page_title="🔊噪音事件稽查儀表板", layout="wide")
viewers = ["經典儀表板", "趨勢優先視角", "左右非對稱佈局", 
            "分頁精簡模式", "地理熱點視角","垂直故事線視角"]
width, height = 600, 450


#-- 建立資料庫連線 --# 
try:
    conn = linkdb()
    repo = ExceedRepository(conn)
    min_time, max_time = repo.get_time_range()
except Exception as e:
    st.error("❌ 無法連線到資料庫，請稍後再試。")
    with st.expander("查看詳細錯誤"):
        st.exception(e)
    st.stop()  

#-- Sidebar --# 
layout_mode,filtered_df = render_sidebar(repo,viewers,min_time,max_time)
df = pd.DataFrame(filtered_df)
data               = casecount(df, 'determination')                ### Metric1: 預先計算案件總數，供指標卡使用
fig_area           = politicalarea_chart(df, width, height)        ### Chart 1: 行政區層級結構
fig_heatmap        = sunrisehour_chart(df, width, height)          ### Chart 2: Area Hierarchy (Sunburst)
fig_heatmap_detail = sunrisehourday_chart(df, width, height)       ### Chart 2-1. Area Hierarchy (Sunburst) Enhancements
fig_line           = overstandardcount_chart(df)                   ### Chart 3: 每日超標事件次數分佈
(fig_toplmax, 
fig_toprepeat, 
fig_topcrossarea)  = carsnorepeatcount_chart(df, input_number=10)  ### Chart 4,5,6: 針對車牌計算相對應指標

#-- Mainarea --# 
if layout_mode != "左右非對稱佈局":
    st.caption(f"目前判定進度: {data['completion']:.1%}")
    st.progress(data['completion'])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 總件數", f"{data['total']:,}", help="資料庫中的所有案件")
    col2.metric("🟢 有效件", f"{data['valid']:,}", f"{data['valid']/data['total']:.1%}")
    col3.metric("🔴 無效件", f"{data['invalid']:,}", f"{data['invalid']/data['total']:.1%}", delta_color="inverse")
    col4.metric("🟡 未判定", f"{data['pending']:,}", f"{data['pending']/data['total']:.1%}", delta_color="off", help="尚未進行有效/無效標記的案件")
    st.markdown("---")
figs = {
    "area": fig_area,
    "heatmap": fig_heatmap,
    "heatmap_detail": fig_heatmap_detail,
    "line": fig_line,
    "toplmax": fig_toplmax,
    "toprepeat": fig_toprepeat,
    "topcrossarea": fig_topcrossarea
}
render_layout(layout_mode, figs, data)


