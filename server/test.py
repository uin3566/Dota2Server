from sql.sql_operator import SqlOperator
from data.data_center import DataCenter
import gl


if __name__ == '__main__':
    gl.sql_operator = SqlOperator()
    gl.sql_operator.connect()
    d = DataCenter()
    d.refresh_strategy('all')
    d.load_more_strategy('all', '158107')
