import streamlit as st

def render(figs, data):
    fig_area = figs["area"]
    fig_heatmap = figs["heatmap"]
    fig_heatmap_detail = figs["heatmap_detail"]
    fig_line = figs["line"]
    fig_toplmax = figs["toplmax"]
    fig_toprepeat = figs["toprepeat"]
    fig_topcrossarea = figs["topcrossarea"]


    st.markdown("### 🗺️ 重點區域監測")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_area, use_container_width=True)
    with c2:
        st.plotly_chart(fig_heatmap, use_container_width=True)
        with st.expander("查看熱力圖數據源"):
             st.plotly_chart(fig_heatmap_detail, use_container_width=True)

    st.divider()
    
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.markdown("#### 趨勢分析")
        st.plotly_chart(fig_line, use_container_width=True)
    with c_right:
        st.markdown("#### 累犯榜首")
        st.plotly_chart(fig_toprepeat, use_container_width=True) # 只秀最重要的累犯

    with st.expander("查看更多排行榜 (超標王/跨區王)"):
        ec1, ec2 = st.columns(2)
        with ec1:
            st.plotly_chart(fig_toplmax, use_container_width=True)
        with ec2:
            st.plotly_chart(fig_topcrossarea, use_container_width=True)