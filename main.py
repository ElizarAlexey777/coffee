import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coffee.ui', self)
        self.app_data()

    def app_data(self):
        con = sqlite3.connect('coffee_sqlite.db')
        cur = con.cursor()
        query = cur.execute(f'''SELECT ID, Name_sort, D_roasting, Ground_or_In_grains, Descr_of_taste, Price, 
                               Volume_of_package_gr FROM coffee''').fetchall()
        print(query)
        self.upd_data(query)
        con.close()

    def upd_data(self, query):
        row_number = 0
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(query):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if len(query) != 0:
            self.statusBar().showMessage(f'Нашлось {str(row_number + 1)} записей.')
        else:
            self.statusBar().showMessage(f'К сожалению, ничего не нашлось.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())