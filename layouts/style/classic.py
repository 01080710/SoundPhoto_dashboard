import streamlit as st

def render(figs, data):
    fig_area = figs["area"]
    fig_heatmap = figs["heatmap"]
    fig_heatmap_detail = figs["heatmap_detail"]
    fig_line = figs["line"]
    fig_toplmax = figs["toplmax"]
    fig_toprepeat = figs["toprepeat"]
    fig_topcrossarea = figs["topcrossarea"]


    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_area, use_container_width=True)
    with c2:
        st.plotly_chart(fig_heatmap, use_container_width=True)
        with st.popover("詳細數據透視表"):
            st.plotly_chart(fig_heatmap_detail, use_container_width=True)

    st.plotly_chart(fig_line, use_container_width=True)
    c1, c2 ,c3 = st.columns([3,3,3])

    with c1:
        st.plotly_chart(fig_toplmax, use_container_width=True)
    with c2:
        st.plotly_chart(fig_toprepeat, use_container_width=True)
    with c3:
        st.plotly_chart(fig_topcrossarea, use_container_width=True)