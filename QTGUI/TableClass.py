import datetime

import pandas
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QHeaderView, QMessageBox

from QTGUI import TableForm


class TableGUI(QWidget, TableForm.Ui_TableForm):
    def __init__(self, database=None):
        super().__init__()
        self.setupUi(self)
        self.database = database
        self.tableList = self.tableWidget.selectionModel()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.exDataBtn.clicked.connect(self.exportResult)
        self.lineEdit.textChanged.connect(self.searchFilter)

    def setData(self, data=None):
        if self.database is not None:
            data = self.database.queryAllResult()
        self.tableWidget.setRowCount(len(data))
        for row, item in enumerate(data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item.name))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(item.time))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(item.helmet)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(item.head)))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(item.total)))
            for col in range(2, 6):
                self.tableWidget.item(row, col).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def getIndexs(self):
        items = self.tableList.selectedIndexes()
        for item in items:
            print(self.tableWidget.item(item.row(), item.column()).text())
        # for item in dir(items[0]):
        #     print(item)

    def exportResult(self):
        items = self.tableList.selectedIndexes()
        ids = []
        colNum = self.tableWidget.columnCount()
        for index in range(len(items)):
            if index % colNum == 0:
                temp = self.tableWidget.item(items[index].row(), items[index].column()).text()
                ids.append(int(temp))
        resultStatement = self.database.queryResultByIds(ids)
        resultsDF = pandas.read_sql_query(sql=resultStatement, con=self.database.engine)
        resultCount = 0
        dataCount = 0
        if len(resultsDF) > 0:
            resultsDF.columns = ['检测编号', '文件名', '检测时间', '佩戴安全帽总人数', '未佩戴安全帽总人数', '总人数']
            tagTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            resultsDF.to_excel('./data/' + '分析记录_' + tagTime + '.xlsx', index=False)
            resultCount = len(resultsDF)
        for vid in ids:
            dataDF = pandas.read_sql_query(sql=self.database.queryDataById(vid), con=self.database.engine)
            if len(dataDF) > 0:
                dataDF.columns = ['编号', '分析记录号', '报警时刻', '佩戴安全帽总人数', '未佩戴安全帽总人数',
                                  '总人数']
                dataDF = dataDF.drop(columns='编号')
                tagTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                dataDF.to_excel('./data/' + '详细记录_' + str(vid) + '_' + tagTime + '.xlsx', index=False)
                dataCount = dataCount + 1
        QMessageBox.information(self, '数据导出结果', "共导出{}条分析记录,\n{}条详细记录到data目录下".format(resultCount,dataCount), QMessageBox.Ok,
                                        QMessageBox.Ok)

    def searchFilter(self):
        content = self.lineEdit.text()
        if len(content) > 1:
            findItems = self.tableWidget.findItems(content, Qt.MatchContains)
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHidden(row, True)
            for item in findItems:
                self.tableWidget.setRowHidden(item.row(), False)

        elif len(content) == 0:
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHidden(row, False)
