
import pymysql

config = dict(
    host = 'localhost',
    user = 'root',
    password = '000630',
    database = 'convdb',
    charset = 'utf8'
)

class DB:
    def __init__(self, **CONFIG):
        self.config = CONFIG

    def connect(self):
        return pymysql.connect(**self.config)
    
    # 값 추적
    def verify_list(self, id, name):
        sql = "SELECT COUNT(*) FROM convtb WHERE id=%s or name=%s"
        with self.connect() as con:
            with con.cursor() as cur:
                cur.execute(sql, (id, name))
                count, = cur.fetchone() # 자료형이 튜플임.
                return count == 1

    def find_list(self, id_or_name):
        sql_id = "SELECT * FROM convtb WHERE id=%s"
        sql_name = "SELECT * FROM convtb WHERE name=%s"
        with self.connect() as con:
            with con.cursor() as cur:
                try:
                    if id_or_name.isdigit():
                        cur.execute(sql_id, int(id_or_name))
                    else:
                        cur.execute(sql_name, id_or_name)
                    return cur.fetchall()
                except Exception:
                    return False
    
    # 정렬 ( ID순, 재고순 )
    def fetch_list_id(self):
        sql = "SELECT * FROM convtb ORDER BY id"
        with self.connect() as con:
            with con.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    def fetch_list_nowEA(self):
        sql = "SELECT * FROM convtb ORDER BY nowEA"
        with self.connect() as con:
            with con.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    # 값 추가            
    def insert_list(self, name, price, nowEA):
        sql = "INSERT INTO convtb (name, price, nowEA) VALUES (%s, %s, %s)"
        with self.connect() as con:
            try:
                with con.cursor() as cur:
                    cur.execute(sql, (name, price, nowEA))
                con.commit()
                return True
            except Exception:
                con.rollback()
                return False
    
    # 값 수정
    def update_list(self, id, name=None, price=None, nowEA=None):
        sql_first = "UPDATE convtb SET "
        sql_last = " WHERE id=%s"

        set_clauses = []
        values = []

        if name:  # 빈 문자열은 False 취급됨
            set_clauses.append("name=%s")
            values.append(name)

        if price:
            set_clauses.append("price=%s")
            values.append(price)

        if nowEA is not None:  # spinbox는 숫자니까 None 체크
            set_clauses.append("nowEA=%s")
            values.append(nowEA)

        if not set_clauses:  # 바꿀 게 없으면 종료
            return False

        sql = sql_first + ", ".join(set_clauses) + sql_last
        values.append(id)

        with self.connect() as con:
            try:
                with con.cursor() as cur:
                    cur.execute(sql, values)
                    affected = cur.rowcount  # 영향을 받은 행 수
                if affected == 0:
                    # id가 존재하지 않아 업데이트된 행이 없던 경우
                    con.rollback()
                    return False
                con.commit()
                return True
            except Exception as e:
                print("오류 코드>", e)
                con.rollback()
                return False
    
    # 값 제거
    def delete_list(self, id_or_name):
        acs = "set sql_safe_updates=0;"
        sql_id = "DELETE FROM convtb WHERE id=%s"
        sql_name = "DELETE FROM convtb WHERE name=%s"
        with self.connect() as con:
            try:
                with con.cursor() as cur:
                    cur.execute(acs)
                    if id_or_name.isdigit():
                        cur.execute(sql_id, int(id_or_name))
                    else:
                        cur.execute(sql_name, id_or_name)
                    con.commit()
                    return True
            except Exception:
                con.rollback()
                return False