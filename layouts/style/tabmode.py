import streamlit as st

def render(figs, data):
    fig_area = figs["area"]
    fig_heatmap = figs["heatmap"]
    fig_heatmap_detail = figs["heatmap_detail"]
    fig_line = figs["line"]
    fig_toplmax = figs["toplmax"]
    fig_toprepeat = figs["toprepeat"]
    fig_topcrossarea = figs["topcrossarea"]


    tab1, tab2, tab3 = st.tabs(["📈 趨勢與分佈", "🏆 違規排行榜", "🗺️ 地理細節"])
    
    with tab1:
        st.markdown("##### 時間趨勢")
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("##### 區域概況")
        st.plotly_chart(fig_area, use_container_width=True)    
    with tab2:
        st.markdown("##### 三大重點排行")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(fig_toplmax, use_container_width=True)
        with c2:
            st.plotly_chart(fig_toprepeat, use_container_width=True)
        with c3:
            st.plotly_chart(fig_topcrossarea, use_container_width=True)  
    with tab3:
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.plotly_chart(fig_heatmap_detail, use_container_width=True)