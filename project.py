from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import sys
import mysql.connector as con

# import UI interface
ui, _ = loadUiType('UI.ui')

# Database password
pwd = "P76101322"


entity_name = ['therapist', 'patient', 'dependent', 'assessment', 'treatment', 'make_assess', 'make_treat']


# Entity attributes
therapist = ['therapist_id', 'first_name', 'last_name', 'sex', 'birth', 'ssn', 'phone', 'address', 'join_date', 'salary']
patient = ['patient_id', 'first_name', 'last_name', 'sex', 'birth', 'ssn', 'phone', 'address', 'attend_therapist']
dependent = ['Essn', 'first_name', 'sex', 'ssn', 'phone', 'relationship']
assessment = ['id', 'assessment_name', 'price', 'duration']
treatment = ['id', 'treat_name', 'price', 'duration']
make_assess = ['id', 'therapist_id', 'patient_id', 'assess_name', 'assess_date', 'description', 'price']
make_treat = ['id', 'therapist_id', 'patient_id', 'treat_name', 'treat_date', 'description', 'price']


class MainApp(QWidget, ui):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.query_tools_ui()
        self.pushButton.clicked.connect(self.show_table)
        self.tool_button.clicked.connect(self.button_show_table)
        self.clear_button.clicked.connect(self.clean_table)

        # Hide label
        self.tool_label.hide()
        self.keyword_label.hide()


    # Set bar choices
    def query_tools_ui(self):

        queries = ['SELECT-FROM-WHERE', 'DELETE', 'INSERT','UPDATE', 'IN', 'NOT IN', 'EXISTS', 'NOT EXISTS', 'COUNT', 'SUM', 'MAX',
                    'MIN', 'AVG', 'HAVING']

        self.query_tool.addItems(queries)


    # bar choice which execute the following SQL instructions
    def selection_condition(self,select):

        queries = {

        "SELECT-FROM-WHERE": "select therapist_id, first_name, last_name from therapist where therapist_id = 1;",
        "DELETE": "DELETE FROM assessment where id = 13",
        "INSERT": 'INSERT INTO assessment VALUES(NULL, "Other assessment", 600, 20);',
        "UPDATE": 'update therapist set first_name = "Mao" where first_name = "Maomao";',
        "IN": 'SELECT therapist_id, salary FROM therapist WHERE therapist_id IN (select therapist_id from make_assess where assess_name = "Shoulder assessment" );',
        "NOT IN": 'SELECT therapist_id, salary FROM therapist WHERE therapist_id NOT IN (select therapist_id from make_assess where assess_name = "Shoulder assessment" );',
        "EXISTS": 'SELECT first_name, last_name, ssn FROM therapist WHERE EXISTS (select * from dependent where therapist.ssn = Essn );',
        "NOT EXISTS": 'SELECT first_name, last_name, ssn FROM therapist WHERE NOT EXISTS (select * from dependent where therapist.ssn = Essn );',
        "COUNT": 'SELECT COUNT(distinct patient_id) FROM make_assess where assess_date = "2022-12-30" ',
        "SUM": 'SELECT SUM(price) FROM implement_treat where treat_date = "2022-12-30";',
        "MAX": 'SELECT MAX(salary) FROM therapist where sex = "M";',
        "MIN": 'SELECT MIN(salary) FROM therapist where sex = "F";',
        "AVG": 'SELECT AVG(salary) FROM therapist;',
        "HAVING": 'select assess_name, sum(price) as achievement from make_assess where assess_date = "2022-12-30" group by assess_name having achievement > 500'

        }

        qry = queries[select]
        qry_list = self.get_header(qry)

        return qry, qry_list


    # Present query results from query keywords area
    def show_table(self):
        try:

            mydb = con.connect(host = "localhost", user = "root", password = pwd, db = "clinical_system")

            # Get command and Execute command
            command = self.query_keyword.toPlainText()
            qry_list = self.get_header(command)
            cursor = mydb.cursor()
            cursor.execute(command)
            result = cursor.fetchall()

            # Show Horizontal header
            self.show_query.horizontalHeader().setVisible(True)


            # Show data
            row_count = 0
            col_count = 0

            for i in range(self.show_query.rowCount()):
                self.show_query.removeRow(0)

            for row_number, row_data in enumerate(result):
                row_count += 1
                col_count = 0
                for col_number, col_data in enumerate(row_data):
                    col_count += 1

            self.show_query.clear()
            self.show_query.setColumnCount(col_count)

            for row_number, row_data in enumerate(result):
                self.show_query.insertRow(row_number)

                for col_number, data in enumerate(row_data):
                    self.show_query.setItem(row_number,col_number,QTableWidgetItem(str(data)))

                    # Text in table align to center
                    text = self.show_query.item(row_number,col_number)
                    text.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


            # Set column width
            for i in range(self.show_query.rowCount()):
                self.show_query.setColumnWidth(i, 220)


            # Show message and align to center
            self.keyword_label.setText(command + "  successfully!")
            self.keyword_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.keyword_label.show()

            # Set query header label
            self.show_query.setHorizontalHeaderLabels(qry_list)
            self.show_query.verticalHeader().setVisible(False)
            mydb.commit()

        except Exception as e:
            print(e)


    def button_show_table(self):

        try:

            mydb = con.connect(host = "localhost", user = "root", password = pwd, db = "clinical_system")

            # Get command and Execute command
            command = self.query_tool.currentText()
            qry_list = self.get_header(command)
            qry,qry_list = self.selection_condition(command)
            cursor = mydb.cursor()
            cursor.execute(qry)
            result = cursor.fetchall()

            # Show Horizontal header
            self.show_query.horizontalHeader().setVisible(True)


            # Show data
            row_count = 0
            col_count = 0

            for i in range(self.show_query.rowCount()):
                self.show_query.removeRow(0)

            for row_number, row_data in enumerate(result):
                row_count += 1
                col_count = 0
                for col_number, col_data in enumerate(row_data):
                    col_count += 1

            self.show_query.clear()
            self.show_query.setColumnCount(col_count)

            for row_number, row_data in enumerate(result):
                self.show_query.insertRow(row_number)

                for col_number, data in enumerate(row_data):
                    self.show_query.setItem(row_number,col_number,QTableWidgetItem(str(data)))

                    # Text in table align to center
                    text = self.show_query.item(row_number,col_number)
                    text.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


            # Set column width
            for i in range(self.show_query.rowCount()):
                self.show_query.setColumnWidth(i, 220)


            # Show message and align to center
            self.tool_label.setText(qry + "  successfully!")
            self.tool_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tool_label.show()

            # Set query header label
            self.show_query.setHorizontalHeaderLabels(qry_list)
            self.show_query.verticalHeader().setVisible(False)
            mydb.commit()


        except Exception as e:
            print(e)



    # Clean query table contents
    def clean_table(self):
        self.show_query.horizontalHeader().setVisible(False)
        for i in range(self.show_query.rowCount()):
                self.show_query.removeRow(0)



    # Get table header name
    def get_header(self,input_string):

        header = []
        get_sentence = input_string.split()

        select_index = -1
        from_index = -1
        where_index = -1


        # Record select, from, where index
        for i in range(len(get_sentence)):
            if get_sentence[i].lower() == 'select':
                select_index = i
                break

        for j in range(len(get_sentence)):
            if get_sentence[j].lower() == 'as' or get_sentence[j].lower() == 'from':
                from_index = j
                break

        for w in range(len(get_sentence)):
            if get_sentence[w].lower() == 'where':
                where_index = w
                break


        # Show * table header
        if get_sentence[select_index + 1] == '*':
            if where_index == -1:
                for h in range(from_index+1, len(get_sentence)):
                    get_sentence[h] = self.clean_sentence(get_sentence[k])
                    tmp_list = self.select_entity(get_sentence[h],entity_name)
                    header = header + tmp_list

            else:
                for v in range(from_index+1, where_index):
                    get_sentence[v] = self.clean_sentence(get_sentence[k])
                    header.append(get_sentence[v])


        # Show specific columns table header
        for k in range(select_index+1,from_index):
            get_sentence[k] = self.clean_sentence(get_sentence[k])
            if get_sentence[k].lower() == 'distinct':
                pass

            else:
                header.append(get_sentence[k])

        return header


    def clean_sentence(self, word):
        return word.lower().replace(',', '')


    def select_entity(self,input_string, selection):

        for i in selection:
            if i == input_string:
                return globals()[input_string]


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()