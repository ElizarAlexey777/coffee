import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coffee.ui', self)
        self.app_data()
        self.initUI()

    def initUI(self):
        self.change_delete_btn.clicked.connect(self.addEditCoffeeForm)

    def addEditCoffeeForm(self):
        sec_w = addEditCoffeeForm()
        sec_w.exec()
        self.rest_db()

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

    def rest_db(self):
        con = sqlite3.connect('coffee_sqlite.db')
        cur = con.cursor()
        query = cur.execute(f'''SELECT ID, Name_sort, D_roasting, Ground_or_In_grains, Descr_of_taste, Price, 
                                       Volume_of_package_gr FROM coffee''').fetchall()
        print(query)
        self.upd_data(query)
        con.close()


class addEditCoffeeForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.add_layout.hide()
        self.comp_btn.hide()
        self.id_layout.hide()
        self.change_layout.hide()
        self.delete_layout.hide()

        self.app_data()
        self.initUI()

    def initUI(self):
        self.add_rb.toggled.connect(lambda: self.edit_form(command='add'))
        self.change_rb.toggled.connect(lambda: self.edit_form(command='change'))
        self.delete_rb.toggled.connect(lambda: self.edit_form(command='delete'))

        self.show()

    def app_data(self):
        con = sqlite3.connect('coffee_sqlite.db')
        cur = con.cursor()
        query = cur.execute(f'''SELECT ID, Name_sort, D_roasting, Ground_or_In_grains, Descr_of_taste, Price, 
                               Volume_of_package_gr FROM coffee''').fetchall()
        self.upd_data(query)
        con.close()

    def upd_data(self, query):
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(query):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def edit_form(self, command):
        if command == 'add':
            self.add_layout.show()
            self.comp_btn.show()
            self.id_layout.hide()
            self.change_layout.hide()
            self.delete_layout.hide()
            self.comp_btn.clicked.connect(self.add)

        if command == 'change':
            self.add_layout.hide()
            self.comp_btn.show()
            self.id_layout.show()
            self.change_layout.show()
            self.delete_layout.hide()
            self.app_cb()
            self.comp_btn.clicked.connect(self.change)

        if command == 'delete':
            self.add_layout.hide()
            self.comp_btn.show()
            self.id_layout.hide()
            self.change_layout.hide()
            self.delete_layout.show()
            self.comp_btn.clicked.connect(self.delete)

    def add(self):
        con = sqlite3.connect('coffee_sqlite.db')
        cur = con.cursor()
        cur.execute('''INSERT INTO coffee(Name_sort, D_roasting, Ground_or_In_grains, Descr_of_taste, Price, Volume_of_package_gr) 
                      VALUES (?, ?, ?, ?, ?, ?)''',
                      (str(self.name_v.text()), str(self.step_v.text()), str(self.mol_zern_v.text()), str(self.descr_taste_v.text()),
                       str(self.price_v.text()), str(self.vol_of_package_v.text()),)).fetchall()
        con.commit()
        con.close()

    def change(self):
        sl = {}
        cb = [c.isChecked() for c in self.cb]
        for idx in range(len(cb)):
            if self.edits[idx].isEnabled():
                sl[f'{self.cb[idx].text()}'] = self.edits[idx].text()
        con = sqlite3.connect('coffee_sqlite.db')
        cur = con.cursor()
        keys = ','.join(sl.keys())
        question_marks = ','.join(list('?' * len(sl)))
        values = tuple(sl.values())
        print(keys, values)
        cur.execute(f'''UPDATE coffee SET ({keys})=({question_marks}) WHERE ID == {self.id_sb.value()}''', values).fetchall()
        con.commit()
        con.close()

    def app_cb(self):
        self.cb = [self.name_cb, self.step_cb, self.mol_zern_cb, self.descr_taste_cb, self.price_cb,
                   self.vol_of_package_cb]
        self.edits = [self.name_v_2, self.step_v_2, self.mol_zern_v_2,
                            self.descr_taste_v_2, self.price_v_2, self.vol_of_package_v_2]
        for ed in self.edits:
            ed.setDisabled(True)
        for check in self.cb:
            check.stateChanged.connect(self.checked_state)

    def checked_state(self, state):
        check = self.sender()
        idx = self.cb.index(check)
        self.edits[idx].setDisabled(False if state == 2 else True)
        if self.edits[idx].isEnabled() is False:
            self.edits[idx].setText('')

    def delete(self):
        con = sqlite3.connect('coffee_sqlite.db')
        cur = con.cursor()
        cur.execute(f'''DELETE FROM coffee WHERE ID == {self.id_del_sb.value()}''').fetchall()
        con.commit()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())