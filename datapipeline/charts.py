from datapipeline.feature_engineer import (politicalarea,
                                           sunrisehour,
                                           sunrisehourday,
                                           overstandardcount,
                                           carsnorepeatcount)
import plotly.graph_objects as go
import plotly.express as px

# 地址資訊圓餅圖
def politicalarea_chart(df,width=800, height=600): 
    df = politicalarea(df)
    fig_area = px.sunburst(
        df,
        path=['city', 'town', 'street_short'],
        title = "行政區層級結構",
        values='count',
        color='town',  # color 可以依鄉鎮分色
        hover_data=['city', 'town', 'street', 'count'],
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )

    fig_area.update_traces(
        root_color="lightgray",
        textinfo="label+value+percent entry",  # 標籤只顯示名稱 + 百分比
        hovertemplate=(
            "<b>%{label}</b><br>"
            "📍 城市：%{customdata[0]}<br>"
            "🏘 鄉鎮：%{customdata[1]}<br>"
            "🚏 街道：%{customdata[2]}<br>"
            "🔢 數量：%{value}<br>"
            "<extra></extra>"
        ),
        insidetextorientation='radial',  # 文字沿圓形旋轉，避免擠壓
        branchvalues='total',  # 層級值按總數比例顯示
    )

    fig_area.update_layout(
        width=width,   # 圖寬
        height=height,  # 圖高
        margin=dict(t=60, l=20, r=20, b=20),
        uniformtext=dict(minsize=12, mode='hide'),  # 太小文字自動隱藏
    )


    fig_area.update_layout(
        sunburstcolorway=px.colors.qualitative.Vivid,
        extendsunburstcolors=True
    )
    return fig_area


# 日/小時熱點矩陣圖
def sunrisehour_chart(df, width=800, height=600):
    df1 = sunrisehour(df)
    fig_heatmap = px.density_heatmap(df1, 
                         x="day", 
                         y="hour", 
                         title="每日各時段熱力圖",
                         nbinsx=60, 
                         nbinsy=60,
                         color_continuous_scale="YlGnBu",  # 更鮮豔的色階，可換 Turbo, Cividis, Plasma, Viridis…  YlOrRd ,YlOrBr, YlGnBu
                        histfunc="count",)
    fig_heatmap.update_layout(
        width = width,
        height= height,
        template="plotly_white",
        coloraxis_colorbar=dict(
            title="事件總數",
            tickfont=dict(size=12),
        )
    )

    fig_heatmap.update_yaxes(dtick=1)
    return fig_heatmap



# 小時數量分布柱狀圖
def sunrisehourday_chart(df, width=800, height=600):
    df1, hour_group = sunrisehourday(df)
    fig_heatmap_detail = px.histogram(
        df1,
        x="hour",
        color="day_type",
        barmode="group",
        opacity=0.75,  # 透明度讓圖更亮麗
        title="✨ 平日 vs 假日：每小時數量分布",
        color_discrete_sequence=["#FF9933", "#1F77FF"],  # 更亮麗的橘 & 藍
        template="plotly_white"
    )

    fig_heatmap_detail.update_xaxes(
        dtick=1,
        title="hour",
        showgrid=True,
        gridcolor="rgba(200,200,200,0.3)"
    )

    fig_heatmap_detail.update_yaxes(
        title="count",
        showgrid=True,
        gridcolor="rgba(200,200,200,0.3)"
    )

    fig_heatmap_detail.update_layout(
        width = width,
        height= height,
        legend_title_text="Day Type",
        legend=dict(
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        )
    )

    # 先計算每小時數量
    hour_group = df1.groupby(["hour", "day_type"]).size().reset_index(name="count")

    # 分平日/假日列表
    colors = {"Rest Day": "#FF6600", "Work Day": "#0066FF"}

    for day_type in ["Work Day", "Rest Day"]:
        sub = hour_group[hour_group["day_type"] == day_type]
        fig_heatmap_detail.add_trace(
            go.Scatter(
                x=sub["hour"],
                y=sub["count"],
                mode="lines+markers",
                name=f"{day_type} Trend",
                line=dict(width=3, color=colors[day_type]),
                marker=dict(size=6, color=colors[day_type]),
            )
        ) 

    return fig_heatmap_detail


# 超標86/90分貝mirror圖
def overstandardcount_chart(df):
    df_daily = overstandardcount(df, standard=86)
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Bar(
        x=df_daily['count_86_neg'],
        y=df_daily['date'],
        orientation='h',
        name='86-90 dbA'
    ))
    fig_line.add_trace(go.Bar(
        x=df_daily['count_90'],
        y=df_daily['date'],
        orientation='h',
        name='90↑ dbA'
    ))
    fig_line.update_layout(
        title='每日超標事件次數分佈',
        barmode='relative',
        xaxis=dict(title='次數', dtick=10),#, tickvals=[-10,-5,0,5,10], ticktext=[10,5,0,5,10]),
        yaxis=dict(title='日期')
    )
    # | barmode      | 效果說明                        |
    # | ------------ | --------------------------- |
    # | `'group'`    | 平行排列：不同分類柱子並列，適合比較同一天不同分類數量 |
    # | `'stack'`    | 堆疊排列：不同分類柱子堆疊在一起，總和呈現總量     |
    # | `'relative'` | 堆疊排列，但可以呈現負值（適合蝶形圖）         |
    # | `'overlay'`  | 柱子互相覆蓋，透明度可調節，看重重疊趨勢        |
    # | `'percent'`  | 百分比堆疊：柱子高度固定為100%，呈現比例分布    |
    return fig_line



# 判斷各種指標柱狀圖
def carsnorepeatcount_chart(df, input_number=10):
    top_lmax, top_repeat, cross_area = carsnorepeatcount(df,input_number=input_number)
    fig_toplmax = px.bar(top_lmax, x="carsno", y="lmax", color="lmax",
                title="🚗 超標王 (最高音量 TOP 10)",
                color_continuous_scale="Reds")
    fig_toprepeat = px.bar(top_repeat, x="carsno", y="count", color="count",
                    title="♻️ 累犯王 (違規次數 TOP 10)",
                    color_continuous_scale="Blues")
    fig_topcrossarea = px.bar(cross_area, x="carsno", y="distinct_area_count",
                    color="distinct_area_count",
                    title="🌐 跨區累犯王 (跨區數量 TOP 10)",
                    color_continuous_scale="Viridis")
    return fig_toplmax, fig_toprepeat, fig_topcrossarea