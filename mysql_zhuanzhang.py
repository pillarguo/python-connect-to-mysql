# coding=UTF-8
import MySQLdb
import sys


class Transfer(object):
    def __init__(self, conn):
        self.conn = conn

    def trans(self,from_id,target_id,value):
        try:
            self.check_avai(from_id)
            self.check_avai(target_id)
            self.check_enough(from_id,value)
            self.reduce_money(from_id,value)
            self.add_money(target_id,value)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print e

    def check_enough(self,from_id,value):
        try:

            cur = self.conn.cursor()
            sql_ch='select * from imooc_goddess where id=%s and id>=%s' % (from_id,value)
            print 'here'
            print sql_ch
            cur.execute(sql_ch)
            if cur.rowcount!=1:
                cur.close()
                raise '%s does not have enough money' % from_id
        except Exception as e:
            raise e
        finally:
            cur.close()

    def check_avai(self,one):
        try:
            cur = self.conn.cursor()
            sql_ch='select * from imooc_goddess where id=%s' % one
            print sql_ch
            cur.execute(sql_ch)
            if cur.rowcount!=1:
                cur.close()
                raise 'reduce account does not exist'
        except Exception as e:
            raise e
        finally:
            cur.close()

    def add_money(self,to_one,money):
        try:
            cur=self.conn.cursor()
            sql_add='update imooc_goddess set id=id+%s where id=%s' % (money,to_one)
            print sql_add
            cur.execute(sql_add)
            #cur.close()
        except Exception as e:
            raise e
        finally:
            cur.close()

    def reduce_money(self, from_one,money):
        try:
            cur= self.conn.cursor()
            sql_red='update imooc_goddess set id=id-%s where id=%s' % (money,from_one)
            print sql_red
            cur.execute(sql_red)
        except Exception as e:
            raise e
        finally:
            cur.close()


if __name__=="__main__":
    connection = MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='imooc',
        charset='utf8'
    )

    transfer=Transfer(connection)
    reduce_one=sys.argv[1]
    add_one=sys.argv[2]
    mon=sys.argv[3]
    try:
        transfer.trans(reduce_one,add_one,mon)
    # cursor = conn.cursor()
    # sql_select='select * from imooc_goddess'
    # sql_insert='insert into imooc_goddess(id,user_name) values(7,"zhangsan")'
    # sql_update='update imooc_goddess set user_name="小名" where id=2'
    # sql_delete='delete from imooc_goddess where id=1'
    # try:
    #     cursor.execute(sql_select)
    #     print cursor.rowcount
    #     cursor.execute(sql_insert)
    #     print cursor.rowcount
    #     cursor.execute(sql_update)
    #     print cursor.rowcount
    #     cursor.execute(sql_delete)
    #     print cursor.rowcount
    #     conn.commit()
    # except Exception as e:
    #     print(e)
    #     conn.rollback()
    #
    # cursor.close()
    except Exception as e:
        print e
    finally:
        connection.close()