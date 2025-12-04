import streamlit as st

def render(figs, data):
    fig_area = figs["area"]
    fig_heatmap = figs["heatmap"]
    fig_line = figs["line"]
    fig_toplmax = figs["toplmax"]
    fig_toprepeat = figs["toprepeat"]
    fig_topcrossarea = figs["topcrossarea"]


    st.header("1. 整體趨勢")
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.header("2. 熱點分析")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_area, use_container_width=True)
    with c2:
        st.plotly_chart(fig_heatmap, use_container_width=True)

    st.header("3. 重點違規車輛")
    t1, t2, t3 = st.tabs(["🚗 最高音量", "♻️ 累犯次數", "🌐 跨區行駛"])
    with t1:
        st.plotly_chart(fig_toplmax, use_container_width=True)
    with t2:
        st.plotly_chart(fig_toprepeat, use_container_width=True)
    with t3:
        st.plotly_chart(fig_topcrossarea, use_container_width=True)