from sql.sql_operator import SqlOperator
from data.data_center import DataCenter
from spider.article_detail_processor import ArticleDetailProcessor
import gl


if __name__ == '__main__':
    gl.sql_operator = SqlOperator()
    gl.sql_operator.connect()
    # d = DataCenter()
    # d.refresh_strategy('all')
    # d.load_more_strategy('all', '158107')
    ap = ArticleDetailProcessor()
    ap.get_news_detail_html_body('20160811', '187351')
