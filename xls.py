# -*- coding: utf-8 -*-
# Time    : 2019/3/1 23:20
# Author  : XYZ

import xlwt
import pymysql


class XlsSave:

    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='xyz',
            passwd='131865apple',
            db='china_library',
            charset='utf8',
        )
        self.cursor = self.db.cursor()
        self.save_path = r'D:\国图保存\国图-CLC=p4.xls'
        self.header = ['序号', '头标区', 'ID 号', '通用数据', '题名与责任', '出版项', '载体形态项',
                       '语言', '一般附注', '内容提要', '题名', '主题', '中图分类号', '著者',
                       '附加款目', '馆藏']
        self.xls = xlwt.Workbook()
        self.sheet = self.xls.add_sheet('国图-CLC=p4', cell_overwrite_ok=True)

    def run(self):
        column = 0
        self.cursor.execute("select * from linkdetails")
        res = self.cursor.fetchall()

        # 写入标题
        for i, head in enumerate(self.header):
            self.sheet.write(0, i, label=head)

        for row in res:
            for index, item in enumerate(row):
                self.sheet.write(column + 1, index, item)
            column += 1

        self.xls.save(self.save_path)


x = XlsSave()
x.run()