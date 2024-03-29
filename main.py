from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
import pyodbc


class connetionBD():
    def __init__(self):
        self.query = ["select * from openquery (POSTGRESTEST, 'select * from Auto where YearOfAuto = ''%s'';');"]

    def conectionbd(self):
        conetionr_to_MSSQL = pyodbc.connect(
            r'Driver={SQL Server};Server=DESKTOP-EPARK0G\SQLEXPRESS;Database=ForTraning;'
            r'Trusted_Connection = yes;')
        return conetionr_to_MSSQL

    def SQLquery(self, planeText, comboBoxtCT):
        cursorMSSQL = self.conectionbd()
        cursor = cursorMSSQL.cursor()
        totalres = []
        cursor.execute(self.query[int(comboBoxtCT)] % planeText)  # нужно значение из выпадающего списка
        while True:
            row = cursor.fetchone()
            if not row:
                break
            totalres.append(row)
        cursorMSSQL.close()
        return totalres


class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ConDB = connetionBD()
        self.set()

    def set(self):
        self.w_root = uic.loadUi('MainWindow.ui')
        self.w_root.comboBox.addItems(['0', '1', '2', '3'])
        self.w_root.pushButton.clicked.connect(self.queryBD)
        self.w_root.tableOut.setColumnCount(7)
        self.w_root.tableOut.setRowCount(300)
        self.w_root.tableOut.setHorizontalHeaderLabels(["IDвто","Модель","Год","Мощность",
                                                        "Цена","Ко-во","Магазин"])
        self.w_root.show()

    def queryBD(self):
        planeText = self.w_root.qIN.toPlainText()
        comboBoxtCT = self.w_root.comboBox.currentText()
        list_of_qury = self.ConDB.SQLquery(planeText=planeText, comboBoxtCT=comboBoxtCT)
        self.w_root.tableOut.clear()
        self.w_root.tableOut.setHorizontalHeaderLabels(["IDвто", "Модель", "Год", "Мощность",
                                                        "Цена", "Ко-во", "Магазин"])
        for i, el in enumerate(list_of_qury):
            self.w_root.tableOut.setItem(i, 0, QTableWidgetItem(str(el.idauto)))
            self.w_root.tableOut.setItem(i, 1, QTableWidgetItem(el.model))
            self.w_root.tableOut.setItem(i, 2, QTableWidgetItem(el.yearofauto))
            self.w_root.tableOut.setItem(i, 3, QTableWidgetItem(str(el.powerofauto)))
            self.w_root.tableOut.setItem(i, 4, QTableWidgetItem(str(el.price)))
            self.w_root.tableOut.setItem(i, 5, QTableWidgetItem(str(el.valueofauto)))
            self.w_root.tableOut.setItem(i, 6, QTableWidgetItem(str(el.idstor)))
        #self.w_root.tableOut.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
