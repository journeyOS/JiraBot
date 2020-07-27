#  !/usr/bin/env python
#  -*- encoding: utf-8 -*-
#
#  Copyright (c) 2020 anqi.huang@outlook.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import xlsxwriter

from base import Utils


class WriteExcel:
    def __init__(self):
        """
        初始化一个工作薄
        """
        self.__workbook = xlsxwriter.Workbook(
            "{location}{fileName}.xlsx".format(location=Utils.realPath("../cache/"),
                                               fileName="game_dock_issues"), {'strings_to_numbers': True})
        self.format_date = self.__workbook.add_format(
            {'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_size': 10})  # 时间格式
        self.format_head = self.__workbook.add_format({
            'bold': True,  # 字体加粗
            # 'border': 1,  # 单元格边框宽度
            'align': 'center',  # 对齐方式
            'valign': 'vcenter',  # 字体对齐方式
            'fg_color': '#CBCBFF',  # 单元格背景颜色
            # 'font_size': 12  # 字体大小
        })

        self.format_odd = self.__workbook.add_format({
            'align': 'center',  # 对齐方式
            'valign': 'vcenter',  # 字体对齐方式
            # 'fg_color': '#ebf1de',  # 单元格背景颜色
        })

        self.format_even = self.__workbook.add_format({
            'align': 'center',  # 对齐方式
            'valign': 'vcenter',  # 字体对齐方式
            # 'fg_color': '#d8e4bc',  # 单元格背景颜色
        })

    def __sheet(self, sheet_name):
        """
        创建工作表
        """
        self.__worksheet = self.__workbook.add_worksheet(name=sheet_name)
        return self.__worksheet.set_column("A:Z", 20)

    def __write(self, heads, data):
        """
        写入数据头及数据,自适应数据数组行列
        """
        for index, value in enumerate(heads):
            co = chr(66 + index)
            row = "{colum}{index}".format(colum=co, index=1)
            self.__worksheet.write(str(row), value, self.format_head)

        if len(data) == 1:
            for one, values in enumerate(data):
                for index, value in enumerate(values):
                    co = chr(65 + index)
                    row = "{colum}{index}".format(colum=co, index=2)

                    if (index % 2) == 0:
                        format = self.format_even
                    else:
                        format = self.format_odd

                    self.__worksheet.write(str(row), value, format)
        else:
            for more, values in enumerate(data):
                for index, value in enumerate(values):
                    # print(value)
                    co = chr(65 + index)
                    row = "{colum}{index}".format(colum=co, index=2 + more)
                    if (index % 2) == 0:
                        format = self.format_even
                    else:
                        format = self.format_odd
                    self.__worksheet.write(str(row), value, format)

    def __chart_series(self, sheetName, data):
        """
        制表数据
        area: Creates an Area (filled line) style chart.
        bar: Creates a Bar style (transposed histogram) chart.
        column: Creates a column style (histogram) chart.
        line: Creates a Line style chart.
        pie: Creates a Pie style chart.
        doughnut: Creates a Doughnut style chart.
        scatter: Creates a Scatter style chart.
        stock: Creates a Stock style chart.
        radar: Creates a Radar style chart.
        """
        chartSeries = self.__workbook.add_chart({'type': 'bar'})
        chartSeries.add_series({
            "name": '=%s!$B$1' % '!$B$1',  # 数据名
            "categories": '=' + sheetName + '!$A$2:$A$%s' % (len(data) + 1),  # 数据列长度
            "values": '=' + sheetName + '!$B$2:$B$%s' % (len(data) + 1),  # 数据列值
            'marker': {'type': 'circle', 'size': 10},
            'line': {'color': 'red'},
        })
        chartSeries.add_series({
            "name": '=%s!$B$1' % '!$C$1',  # 数据名
            "categories": '=' + sheetName + '!$A$2:$A$%s' % (len(data) + 1),  # 数据列长度
            "values": '=' + sheetName + '!$C$2:$C$%s' % (len(data) + 1),  # 数据列值
            'marker': {'type': 'circle', 'size': 10},
            'line': {'color': 'yellow'},
        })
        chartSeries.add_series({
            "name": '=%s!$B$1' % '!$D$1',  # 数据名
            "categories": '=' + sheetName + '!$A$2:$A$%s' % (len(data) + 1),  # 数据列长度
            "values": '=' + sheetName + '!$D$2:$D$%s' % (len(data) + 1),  # 数据列值
            'marker': {'type': 'circle', 'size': 10},
            'line': {'color': 'blue'},
        })
        chartSeries.add_series({
            "name": '=%s!$B$1' % '!$E$1',  # 数据名
            "categories": '=' + sheetName + '!$A$2:$A$%s' % (len(data) + 1),  # 数据列长度
            "values": '=' + sheetName + '!$E$2:$E$%s' % (len(data) + 1),  # 数据列值
            'marker': {'type': 'circle', 'size': 10},
            'line': {'color': 'green'},
        })
        chartSeries.set_title({'name': sheetName})  # 图表标题
        chartSeries.set_x_axis({'name': u'处理人'})  # x轴标题
        chartSeries.set_y_axis({'name': u'数量'})  # y轴标题
        return chartSeries

    def __chart(self, sheetName, heads, data):
        """
        绘图
        """
        return self.__worksheet.insert_chart('%s2' % chr(len(heads) + 66), self.__chart_series(sheetName, data),
                                             {'x_offset': 10, 'y_offset': 10})

    def close(self):
        """
        关闭工作薄
        :return:
        """
        self.__workbook.close()

    def writeData(self, sheet_name, heads, data):
        """
        写入流程
        """
        self.__sheet(sheet_name)
        self.__write(heads, data)
        self.__chart(sheet_name, heads, data)
        self.close()
