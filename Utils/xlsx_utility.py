# -*- coding:utf-8 -*-
from openpyxl import load_workbook
import os

class XlsxUtility(object):
	@staticmethod
	def get_sheet_data(xlsx_path, file_name, sheet_num=0, by_column=False):

		workbook = load_workbook(os.path.join(xlsx_path, file_name))
		sheets = workbook.get_sheet_names()  # 从名称获取sheet
		booksheet = workbook.get_sheet_by_name(sheets[sheet_num])

		rows = booksheet.rows
		columns = booksheet.columns
		data = []
		if by_column:
			# 迭代所有的列
			for col in columns:
				data.append([row.value for row in col])
		else:
			# 迭代所有的行
			for row in rows:
				data.append([col.value for col in row])

		return data


