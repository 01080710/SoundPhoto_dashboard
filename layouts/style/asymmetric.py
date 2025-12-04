import streamlit as st

def render(figs, data):
    fig_area = figs["area"]
    fig_heatmap = figs["heatmap"]
    fig_line = figs["line"]
    fig_toplmax = figs["toplmax"]
    fig_toprepeat = figs["toprepeat"]
    fig_topcrossarea = figs["topcrossarea"]


    main_col, side_col = st.columns([3, 1])
    
    with main_col:
        st.caption(f"目前判定進度: {data['completion']:.1%}")
        st.progress(data['completion'])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("總件數", f"{data['total']:,}")
        m2.metric("有效", f"{data['valid']:,}")
        m3.metric("無效", f"{data['invalid']:,}")
        m4.metric("未判定", f"{data['pending']:,}")
        st.markdown("---")
        st.plotly_chart(fig_line, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_area, use_container_width=True)
        with c2:
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with side_col:
        st.markdown("#### 🏆 重點關注名單")
        st.plotly_chart(fig_toplmax, use_container_width=True)
        st.markdown("---")
        st.plotly_chart(fig_toprepeat, use_container_width=True)
        st.markdown("---")
        st.plotly_chart(fig_topcrossarea, use_container_width=True)