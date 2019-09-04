from cone.spider_ex import Recorder, logger
from .settings import MYSQL, TABLE
from cone.sql.pool import MysqlPool
from pymysql import IntegrityError
from cone.spider.item import OriginSqlItem


class _NewsRecorder(object):
    def __init__(self):
        super().__init__()
        self.pool = MysqlPool(**MYSQL)

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
        sql = self.pool.get_sql()
        try:
            sql.cursor.execute(save_cmd)
            sql.conn.commit()
        except IntegrityError:  # 重复
            return False
        except Exception as e:
            logger.error("save error: %s", str(e))
            return False
        finally:
            sql.close()
        return True

    def upadte_item(self, item):
        sql = self.pool.get_sql()
        limit_dict = {'id': item.pop('source_id')}
        code, msg = OriginSqlItem.update_item(sql, TABLE['hotspot-source'], value_dict=item, limit_dict=limit_dict)
        if not code:
            logger.error("update status error, %s", msg)
        sql.close()

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
        self.pool.close()


NewsRecorder = _NewsRecorder()
