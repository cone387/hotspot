from cone.spider_ex import Recorder, logger
from .settings import MYSQL, TABLE
from cone.sql.pool import MysqlPool
from pymysql import IntegrityError
from cone.spider.item import OriginSqlItem


class _NewsRecorder(object):
    def __init__(self):
        super().__init__()
        self.pool = MysqlPool(**MYSQL)
        self.sql = self.pool.get_sql()

    def record(self, item):
        is_test = item.pop('is_test', False)
        table = TABLE['test-hotspot'] if is_test else TABLE['hotspot']
        logger.debug(item)
        return self.save(table, item)

    def record_log(self, log_item):
        if not log_item.pop('is_test'):
            return self.save(TABLE['log-table'], log_item)
        return False

    def save(self, table, item):
        save_cmd = self.get_save_cmd(table, item)
        try:
            self.sql.cursor.execute(save_cmd)
            self.sql.conn.commit()
        except IntegrityError:  # 重复
            return False
        except Exception as e:
            self.sql.close()
            self.sql = self.pool.get_sql()
            logger.error("save error: %s", str(e))
            return False
        return True

    def upadte_item(self, item):
        limit_dict = {'id': item.pop('source_id')}
        code, msg = OriginSqlItem.update_item(self.sql, TABLE['hotspot-source'], value_dict=item, limit_dict=limit_dict)
        if not code:
            logger.error("update status error, %s", msg)

    @classmethod
    def get_save_cmd(cls, table, item):
        names = []
        values = []
        for key, value in item.items():
            names.append(key)
            values.append("'{}'".format(value))
        insert_str = ','.join(names)
        value_str = ','.join(values)
        cmd = 'insert into {}({}) values({})'.format(
            table, insert_str, value_str
        )
        return cmd

    def close(self):
        self.sql.close()
        self.pool.close()


NewsRecorder = _NewsRecorder()
