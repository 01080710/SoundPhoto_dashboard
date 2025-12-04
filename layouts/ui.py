from datapipeline.feature_engineer import generate_export_report
import streamlit as st
import pandas as pd

def render_sidebar(repo,min_time, max_time):
    with st.sidebar:    
        
        viewers = ["經典儀表板", "趨勢優先視角", "左右非對稱佈局", 
                    "分頁精簡模式", "地理熱點視角","垂直故事線視角"]
        layout_mode = viewers[3]
        st.subheader("數據篩選")
        with st.container(border=True):
            start, end = st.slider(
                "🕒 時間區間",
                min_value=min_time, 
                max_value=max_time,
                value=(min_time, max_time),
                format="YYYY-MM-DD"
            )
            
        sites = repo.get_sites(start, end)
        with st.expander("📍 移動站點", expanded=False):
            sites_button = st.multiselect(
                "", options=sites, default=sites,
                placeholder="請選擇..."
            )
            st.caption(f"已選擇 {len(sites_button)} 個站點")

        reasons = repo.get_reasons(start, end)
        with st.expander("⚠️ 事件類型", expanded=False):
            reasons_button = st.multiselect("", options=reasons, default=reasons)
            st.caption(f"已選擇 {len(reasons_button)} 個事件類型")
        
        with st.expander("📏 標準類型", expanded=False):
            noise_button = st.radio("噪音標準", ["超過 86dB", "超過 90dB"])
            wind_button  = st.radio("風速判定", ["大於0.5m/s","小於0.5m/s"], horizontal=True)
            temp_button  = st.slider("溫度範圍", 0, 94, (30,35))
            wind_compare = ">=" if wind_button == "大於0.5m/s" else "<"
            like_conditions = " OR ".join([f"reason LIKE '%{reason}%'" if reason != '' else "reason LIKE ''" for reason in reasons_button] ) if reasons_button else "1=1"
            filtered_df = repo.get_filtered_data(start,
                                                end, 
                                                sites = sites_button, 
                                                like_conditions = like_conditions,                                         
                                                noise_level =  '86'   if noise_button == '超過 86dB' else '90', 
                                                wind_compare= wind_compare,wind_speed  =  str(0.5), 
                                                temp_min = str(temp_button[0]), 
                                                temp_max = str(temp_button[1]))
        st.divider()
        filtered_df = pd.DataFrame(filtered_df)
        if filtered_df.empty:
            st.warning(
                "⚠️ 目前沒有符合篩選條件的資料。\n\n"
                "請調整時間區間、站點或其他篩選條件後再試一次。"
            )
            st.stop()

        st.subheader("數據下載")
        report_df = generate_export_report(filtered_df,start,end)
        csv = report_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="🧾 下載 CSV",
            data=csv,
            file_name=f"噪音稽查數據({start}~{end}).csv",
            mime="text/csv",
        )
        return layout_mode,filtered_df