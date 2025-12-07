from sqlalchemy import text, bindparam
from datetime import datetime


class ExceedRepository:
    def __init__(self, conn):
        self.conn = conn
        
    # 取得資料時間範圍
    def get_time_range(self):
        stmt = text("""
            SELECT MIN(measurementdatetime), MAX(measurementdatetime) 
            FROM exceed
        """)
        start, end = self.conn.execute(stmt).fetchone()

        min_time = datetime.strptime(start, "%Y/%m/%d %H:%M:%S")
        max_time = datetime.strptime(end, "%Y/%m/%d %H:%M:%S")

        return min_time, max_time
    

    # 取得所有站點
    def get_sites(self,db,start,end):
        if db == 'mssql':
            stmt = text("""
                SELECT DISTINCT areaid 
                FROM exceed
                WHERE TRY_CAST(measurementdatetime AS datetime) BETWEEN :start AND :end
                ORDER BY areaid ASC
            """)
        elif db == 'sqlite3':
            stmt = text("""
                SELECT DISTINCT areaid 
                FROM exceed
                WHERE measurementdatetime BETWEEN :start AND :end
                ORDER BY areaid ASC
            """)
        result = self.conn.execute(stmt, {"start": start, "end": end}).fetchall()
        sites = [row[0] for row in result]
        return sites
    

    # 取得所有原因
    def get_reasons(self,db,start,end):
        if db == 'mssql':
            stmt = text("""SELECT
                    CASE
                        WHEN reason IS NULL OR reason IN ('null', '') THEN N'未分類'
                        WHEN reason LIKE '%[a-zA-Z0-9]%' THEN N'未分類'
                        WHEN CHARINDEX(':', reason) > 0 THEN LEFT(reason, CHARINDEX(':', reason) - 1)
                        ELSE reason
                    END AS reason1,
                    COUNT(*) AS count,
                    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage 
                FROM exceed
                WHERE TRY_CAST(measurementdatetime AS datetime) BETWEEN :start AND :end
                GROUP BY
                    CASE
                        WHEN reason IS NULL OR reason IN ('null', '') THEN N'未分類'
                        WHEN reason LIKE '%[a-zA-Z0-9]%' THEN N'未分類'
                        WHEN CHARINDEX(':', reason) > 0 THEN LEFT(reason, CHARINDEX(':', reason) - 1)
                        ELSE reason
                    END
            """)
        elif db == 'sqlite3':
            stmt = text("""
                    SELECT
                    CASE
                        WHEN reason IS NULL OR reason IN ('null', '') THEN '未分類'
                        WHEN reason GLOB '*[A-Za-z0-9]*' THEN '未分類'
                        WHEN instr(reason, ':') > 0 THEN substr(reason, 1, instr(reason, ':') - 1)
                        ELSE reason
                    END AS reason1,
                    COUNT(*) AS count,
                    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
                FROM exceed
                WHERE measurementdatetime BETWEEN :start AND :end
                GROUP BY
                    CASE
                        WHEN reason IS NULL OR reason IN ('null', '') THEN '未分類'
                        WHEN reason GLOB '*[A-Za-z0-9]*' THEN '未分類'
                        WHEN instr(reason, ':') > 0 THEN substr(reason, 1, instr(reason, ':') - 1)
                        ELSE reason
                    END;
            """)
        result = self.conn.execute(stmt, {"start": start, "end": end}).fetchall()
        reasons = [row[0] for row in result]
        return reasons
    


    # 套用所有篩選條件
    def get_filtered_data(self,db,start,end,sites,like_conditions,noise_level, 
                          temp_min, temp_max, wind_compare,wind_speed):
        if db == 'mssql':
            stmt = text(f"""
                    (
                        SELECT *
                        FROM exceed
                        WHERE 
                            TRY_CAST(measurementdatetime AS datetime) BETWEEN :start AND :end
                            AND areaid IN :sites
                            AND lmax >= :noise_level
                            AND (
                                (:wind_compare = '>=' AND windspeed >= :wind_speed)
                                OR (:wind_compare = '<'  AND windspeed <  :wind_speed)
                            )
                            AND tempture BETWEEN :temp_min AND :temp_max
                            AND ({like_conditions})   -- 包含關鍵字
                    )
                    ORDER BY measurementdatetime ASC
                """).bindparams(
                    bindparam("sites", expanding=True)
                )
        elif db == 'sqlite3':
            stmt = text(f"""
                SELECT *
                FROM exceed
                WHERE
                    measurementdatetime BETWEEN :start AND :end
                    AND areaid IN :sites
                    AND lmax >= :noise_level
                    AND (
                        (:wind_compare = '>=' AND windspeed >= :wind_speed)
                        OR (:wind_compare = '<'  AND windspeed <  :wind_speed)
                    )
                    AND tempture BETWEEN :temp_min AND :temp_max
                    AND ({like_conditions})
                ORDER BY measurementdatetime ASC
            """).bindparams(
                bindparam("sites", expanding=True)
            )


        params = {
            'start': start,
            'end': end,
            'sites': tuple(sites),
            'noise_level': noise_level,
            'wind_compare':wind_compare,
            'wind_speed': wind_speed,
            'temp_min': temp_min,
            'temp_max': temp_max
        }

        return self.conn.execute(stmt, params).fetchall()
    

      
      