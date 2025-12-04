from dataquery.transformer import parse_city, parse_town, parse_street
import pandas as pd
import numpy as np

# 計算資料庫萃取出數據總量
def casecount(df: pd.DataFrame, column: str) -> pd.DataFrame:
    total_count = len(df)
    if total_count > 0:
        total_count = df[column].notna().sum()
        valid_mask = df[column].str.contains('有效', na=False)
        invalid_mask = df[column].str.contains('無效', na=False)
        valid_count = valid_mask.sum()
        invalid_count = invalid_mask.sum()
        pending_count = total_count - valid_count - invalid_count  # 自動計算
        completion_rate = (valid_count + invalid_count) / total_count
    else:
        valid_count = invalid_count = pending_count = 0
        completion_rate = 0

    data = {"total": total_count, 
            "valid": valid_count, 
            "invalid": invalid_count, 
            "pending": pending_count, 
            "completion": completion_rate}
    
    return data
    
# 產製相關檔案
def generate_export_report(df: pd.DataFrame,start:str,end:str):
    # Build per-area report using groupby and vectorized operations (faster, safer)
    if df.empty:
        return pd.DataFrame()

    first_dba = ''
    if 'dba' in df.columns:
        non_null_dba = df['dba'].dropna().unique()
        first_dba = non_null_dba[0] if len(non_null_dba) > 0 else ''


    case_stats = df.groupby('areaname').apply(lambda g: pd.Series(casecount(g, 'determination'))).reset_index()

    reason_series = df['reason'].fillna('')
    flags = pd.DataFrame({
        '超標': reason_series.str.contains('超標', na=False),
        '二改': reason_series.str.contains('二改', na=False),
        '通知到檢': reason_series.str.contains('通知到檢', na=False),
        '直接開罰': reason_series.str.contains('直接開罰', na=False),
    }, index=df.index)

    flags['areaname'] = df['areaname']
    reason_counts = flags.groupby('areaname').sum().reset_index()
    report = case_stats.merge(reason_counts, on='areaname', how='left').fillna(0)
    return pd.DataFrame({
        '開始時間': [start] * len(report),
        '結束時間': [end] * len(report),
        '管制標準': [first_dba] * len(report),
        '執行地點': report['areaname'],
        '總計事件': report['total'].astype(int),
        '有效事件': report['valid'].astype(int),
        '無效事件': report['invalid'].astype(int),
        '未判事件': report['pending'].astype(int),
        '超標': report['超標'].astype(int),
        '二改': report['二改'].astype(int),
        '通知到檢': report['通知到檢'].astype(int),
        '直接開罰': report['直接開罰'].astype(int),
    })

# 地址資訊圓餅圖 - 數據清理
def politicalarea(df: pd.DataFrame) -> pd.DataFrame:
    """
    對包含地址資訊的DataFrame進行特徵工程，解析出縣市、鄉鎮市區及街道名稱。

    參數:
    df (pd.DataFrame): 包含地址資訊的DataFrame，需包含'address'欄位。

    回傳:
    pd.DataFrame: 新增'city', 'town', 'street'欄位的DataFrame。
    """
    df['city'] = df['areaname'].apply(parse_city) if 'areaname' in df.columns else '其他'
    df['town'] = df['areaname'].apply(parse_town) if 'areaname' in df.columns else '其他'
    df['street'] = df['areaname'].apply(parse_street) if 'areaname' in df.columns else '其他'
    column = ['city','town','street']
    df1 = df.groupby(column)['measurementdatetime'].size().reset_index(name='count') if 'measurementdatetime' in df.columns else pd.DataFrame(columns=column+['count'])
    df1['street_short'] = df1['street'].apply(lambda x: x if len(x)<=3 else x[:3]+'…')
    return df1

# 日/小時熱點矩陣圖 - 數據清理
def sunrisehour(df: pd.DataFrame) -> pd.DataFrame:
    """
    對包含時間資訊的DataFrame進行特徵工程，解析出日出小時。

    參數:
    df (pd.DataFrame): 包含時間資訊的DataFrame，需包含'measurementdatetime'欄位。

    回傳:
    pd.DataFrame: 新增'sunrise_hour'欄位的DataFrame。
    """
    df['date'] = pd.to_datetime(df['measurementdatetime'])
    df['day_of_month'] = df['date'].dt.isocalendar()['day']
    df['day'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    datelist = ['date','day_of_month','day','hour']
    df1 = df[datelist].sort_values(by='day_of_month')
    return df1


# 小時數量分布柱狀圖 - 數據清理
def sunrisehourday(df: pd.DataFrame) -> pd.DataFrame:
    """
    對包含時間資訊的DataFrame進行特徵工程，解析出日出小時及星期幾。

    參數:
    df (pd.DataFrame): 包含時間資訊的DataFrame，需包含'measurementdatetime'欄位。

    回傳:
    pd.DataFrame: 新增'sunrise_hour'及'day'欄位的DataFrame。
    """
    df1 = sunrisehour(df)

    df1['day_type'] = df1['day_of_month'].apply(lambda x: 'Rest Day' if x in [5,6] else 'Work Day')
    hour_group = df1.groupby(["hour", "day_type"]).size().reset_index(name="count")
    
    return df1, hour_group

# 超標86/90分貝mirror圖 - 數據清理
def overstandardcount(df: pd.DataFrame, standard: float) -> pd.DataFrame:
    """
    計算每日期的超標事件次數。

    參數:
    df (pd.DataFrame): 包含時間及測量值資訊的DataFrame，需包含'measurementdatetime'及'measurementvalue'欄位。
    standard (float): 超標的標準值。

    回傳:
    pd.DataFrame: 包含每日超標事件次數的DataFrame。
    """
    df["date"] = pd.to_datetime(df["measurementdatetime"]).dt.date
    df["lmax"] = pd.to_numeric(df["lmax"], errors='coerce').astype(float)

    conditions = [df['lmax'] > 90, (df['lmax'] >= standard) & (df['lmax'] <= 90), df['lmax'] < standard]
    choices = ['超過90', '超標', '未超標']
    df['overstandard_flag'] = np.select(conditions, choices)
    df_over_86 = df[df['overstandard_flag']=='超標'].groupby('date').size().reset_index(name='count_86')
    df_over_90 = df[df['overstandard_flag']=='超過90'].groupby('date').size().reset_index(name='count_90')
    df_daily = pd.merge(df_over_86, df_over_90, on='date', how='outer').fillna(0)
    df_daily['count_86_neg'] = -df_daily['count_86']
    return df_daily

# 判斷各種指標柱狀圖 - 數據清理
def carsnorepeatcount(df: pd.DataFrame,input_number = 10) -> pd.DataFrame:
    """
    計算每個車牌的重複出現次數。

    參數:
    df (pd.DataFrame): 包含車牌資訊的DataFrame，需包含'carsno'欄位。

    回傳:
    pd.DataFrame: 包含每個車牌及其重複出現次數的DataFrame。
    """
    
    filter_column = ['measurementdatetime','carsno','lmax']
    top_lmax = df.sort_values(by='lmax',ascending=False).head(input_number)[filter_column]  # 超標王
    top_repeat = (df.groupby('carsno')['lmax']
                .size()
                .reset_index(name='count')
                .sort_values(by='count',ascending=False)
                .head(input_number)) # 累犯王
    count_df = df.groupby('carsno')['town'].nunique().reset_index(name='distinct_area_count') # 連續累犯
    list_df = df.groupby('carsno')['town'].apply(lambda x: sorted(x.unique())).reset_index(name='area_list')
    cross_area = ( 
        count_df
        .merge(list_df, on='carsno')
        .sort_values(by='distinct_area_count', ascending=False)
        .head(input_number)
    )
    return top_lmax, top_repeat, cross_area