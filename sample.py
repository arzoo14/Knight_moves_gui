from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView , QMessageBox
from PyQt5.QtGui import QPixmap
import copy
def generatePath(source, target, n):  # source, target = (i,j); n=size
    path = [source]
    bufferQueue = [(source[0],source[1],path)]  # backward search
    done = []
    while bufferQueue:
        underProcessing = bufferQueue.pop()
        if underProcessing[0] == target[0] and underProcessing[1] == target[1]:
            return underProcessing[2]
        for eachNeighbor in getNeighbors(underProcessing, n):
            path_ = copy.copy(underProcessing[2])
            if eachNeighbor in done:
                continue
            else:
                done.append((underProcessing[0], underProcessing[1]))
                path_.append((eachNeighbor[0],eachNeighbor[1]))
                bufferQueue.append((eachNeighbor[0], eachNeighbor[1], path_))
    return {}  # no path

def getNeighbors(location, n):
  neighbors = []
  i, j = location[0], location[1]
  for k, l in ( (i+2,j+1), (i+2,j-1), (i+1,j+2), (i+1,j-2), (i-1,j+2), (i-1,j-2), (i-2,j+1), (i-2,j-1) ):
    if k>=0 and k<n and l>=0 and l<n:
      neighbors.append( (k, l) )
  return neighbors

def printPath(source, paths):
    print(paths)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1000,600);
        self.table = QtWidgets.QTableWidget(Dialog)
        self.table.setGeometry(160, 20, 810, 570);
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(10, 40, 30, 30);
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(40, 40, 30, 30);
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(10, 200, 30, 30);
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(40, 200, 30, 30);
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(40, 500, 95, 30);
        self.pushButton.setObjectName("pushButton")
        self.labelInput = QtWidgets.QLabel("Input coordinates",Dialog)
        self.labelInput.setGeometry(10, 10, 150, 30);
        self.labelOutput = QtWidgets.QLabel("Output coordinates",Dialog)
        self.labelOutput.setGeometry(10, 180, 150, 30);

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setText(_translate("Dialog", ""))
        self.lineEdit_2.setText(_translate("Dialog", ""))
        self.lineEdit_3.setText(_translate("Dialog", ""))
        self.lineEdit_4.setText(_translate("Dialog", ""))
        self.pushButton.setText(_translate("Dialog", "Show Moves"))

    def populate_table(self, Dialog):
        self.table.setRowCount(8);
        self.table.setColumnCount(8);
        self.table.setGeometry(160, 20, 810, 570);
        self.table.horizontalHeader().hide();
        self.table.verticalHeader().hide();
        rowH=70
        for i in range(8):
            self.table.setRowHeight(i,rowH)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            flag=0;
            if i%2 == 0:
                flag=0
            else:
                flag=1
            for j in range(8):
                if flag == 1:
                    pix = QPixmap('images/white.png')
                    label1 = QtWidgets.QLabel()
                    label1.setPixmap(pix)
                    self.table.setCellWidget(i,j,label1)
                else:
                    pix1 = QPixmap('images/black.jpg')
                    label2 = QtWidgets.QLabel()
                    label2.setPixmap(pix1)
                    self.table.setCellWidget(i,j,label2)
                flag=1-flag
    def update_table(self, Dialog, a, b,icon):
                self.table.removeCellWidget(a,b)
                pix = QPixmap(icon)
                label1 = QtWidgets.QLabel()
                label1.setPixmap(pix)
                self.table.setCellWidget(a,b,label1)

    def button_action(self, Dialog):
        self.populate_table(Dialog)
        if not self.lineEdit.text() or not self.lineEdit_2.text() or not self.lineEdit_3.text() or not self.lineEdit_4.text():
            msg = QMessageBox()
            msg.setWindowTitle("Error message")
            msg.setText("Some coordinates are empty, kindly re entered")
            msg.exec_()
            return
        sa, sb = int(self.lineEdit.text()), int(self.lineEdit_2.text())
        ta, tb = int(self.lineEdit_3.text()), int(self.lineEdit_4.text())
        print(sa, sb, ta, tb)
        if sa<0 or sa>7 or sb < 0 or sb>7 or ta<0 or ta>7 or tb<0 or tb>7:
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            msg = QMessageBox()
            msg.setWindowTitle("Error message")
            msg.setText("You have entered wrong coordinates, kindly re entered the values")
            msg.exec_()
            return
        source = (int(self.lineEdit.text()), int(self.lineEdit_2.text()))
        target = (int(self.lineEdit_3.text()), int(self.lineEdit_4.text()))
        path = generatePath(source, target, 8)
        for path_ in path:
            if path_[0] == sa and path_[1] == sb:
                self.update_table(Dialog, path_[0], path_[1], "images/start.png")
            elif path_[0] == ta and path_[1] == tb:
                self.update_table(Dialog, path_[0], path_[1], "images/end.png")
            else:
                self.update_table(Dialog, path_[0], path_[1], "images/knight.png")

from functools import partial
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.populate_table(Dialog)
    ui.pushButton.clicked.connect(partial(ui.button_action, Dialog))
    Dialog.show()
    sys.exit(app.exec_())

