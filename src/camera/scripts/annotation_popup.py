import sys
import random as rd
import math

import trash_item

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CreateAnnotationPopUp(QDialog):
    def __init__(self, x, y):
        super().__init__()
        self.classes = ['Cardboard', 'Metal', 'Rigid Plastic', 'Soft Plastic']
        self.label = 0
        self.width = 220
        self.height = 150
        self.left = x + 10
        self.top = y + 10

        QDialog.__init__(self)
        self.setWindowTitle("Create Annotation")
        self.setGeometry(self.left, self.top, self.width, self.height)
        verticalLayout = QVBoxLayout(self)
        self.text = QLabel()
        self.text.setText(
            'Select type of recycling')
        verticalLayout.addWidget(self.text)

        # Create radio buttons for each class
        self.c0 = QRadioButton(self.classes[0])
        self.c1 = QRadioButton(self.classes[1])
        self.c2 = QRadioButton(self.classes[2])
        self.c3 = QRadioButton(self.classes[3])
        button_list = [self.c0, self.c1, self.c2, self.c3]
        button_list[0].setChecked(True)

        verticalLayout.addWidget(self.c0)
        verticalLayout.addWidget(self.c1)
        verticalLayout.addWidget(self.c2)
        verticalLayout.addWidget(self.c3)
        self.c0.toggled.connect(lambda: self.btnstate(self.c0))
        self.c1.toggled.connect(lambda: self.btnstate(self.c1))
        self.c2.toggled.connect(lambda: self.btnstate(self.c2))
        self.c3.toggled.connect(lambda: self.btnstate(self.c3))

        buttonBox = QDialogButtonBox(self)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        verticalLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.initCreateAnnot()

    def initCreateAnnot(self):
        if self.exec():
            print("Created trash_item type: ", self.label)
        else:
            self.label = -1

    def btnstate(self, b):
        if b.isChecked() == True:
            self.label = self.classes.index(b.text())


class EditAnnotationPopUp(QDialog):
    def __init__(self, trash_item, trash_items):
        super().__init__()
        self.classes = ['Cardboard', 'Metal', 'Rigid Plastic', 'Soft Plastic']
        self.trash_item = trash_item
        self.trash_items = trash_items
        self.updated_conf = self.trash_item.conf
        self.updated_label = self.trash_item.trash_type
        self.delete = False
        self.width = 220
        self.height = 200
        self.left = trash_item.x + 10
        self.top = trash_item.y + 10

        QDialog.__init__(self)
        self.setWindowTitle("Edit Annotation")
        self.setGeometry(self.left, self.top, self.width, self.height)
        verticalLayout = QVBoxLayout(self)

        # Create radio buttons for each class
        self.text = QLabel()
        self.text.setText(
            'Select type of recycling:')
        verticalLayout.addWidget(self.text)
        self.c0 = QRadioButton(self.classes[0])
        self.c1 = QRadioButton(self.classes[1])
        self.c2 = QRadioButton(self.classes[2])
        self.c3 = QRadioButton(self.classes[3])
        button_list = [self.c0, self.c1, self.c2, self.c3]
        button_list[self.trash_item.trash_type].setChecked(True)
        verticalLayout.addWidget(self.c0)
        verticalLayout.addWidget(self.c1)
        verticalLayout.addWidget(self.c2)
        verticalLayout.addWidget(self.c3)
        self.c0.toggled.connect(lambda: self.btnstate(self.c0))
        self.c1.toggled.connect(lambda: self.btnstate(self.c1))
        self.c2.toggled.connect(lambda: self.btnstate(self.c2))
        self.c3.toggled.connect(lambda: self.btnstate(self.c3))

        # Create checkbox to boost confidence
        self.text2 = QLabel()
        self.text2.setText(
            'Adjust confidence 0-100%')
        verticalLayout.addWidget(self.text2)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(self.trash_item.conf)
        # self.slider.setTickPosition(QSlider.TicksBelow)
        # self.slider.setTickInterval(10)
        min_label = QLabel(self, alignment=Qt.AlignLeft)
        min_label.setText("0")
        max_label = QLabel(self, alignment=Qt.AlignRight)
        max_label.setText("100")
        self.slider.valueChanged.connect(self.valuechange)
        verticalLayout.addWidget(self.slider)
        slider_hbox = QHBoxLayout()
        slider_hbox.addWidget(min_label, Qt.AlignLeft)
        slider_hbox.addWidget(max_label, Qt.AlignRight)
        slider_hbox.addStretch()
        verticalLayout.addLayout(slider_hbox)

        # Create checkbox to delete box
        self.checkBox = QCheckBox(self.tr('Delete annotation'), self)
        verticalLayout.addWidget(self.checkBox)
        self.checkBox.toggled.connect(
            lambda: self.checkboxstate(self.checkBox))

        buttonBox = QDialogButtonBox(self)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        verticalLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.initEditAnnot()

    def initEditAnnot(self):
        if self.exec():
            if self.delete:
                if self.trash_item in self.trash_items:
                    self.trash_items.remove(self.trash_item)
            else:
                self.trash_item.trash_type = self.updated_label
                self.trash_item.conf = self.updated_conf
                self.trash_item.updated = True

    def btnstate(self, b):
        if b.isChecked() == True:
            self.updated_label = self.classes.index(b.text())

    def checkboxstate(self, b):
        self.delete = b.isChecked()

    def valuechange(self):
        self.updated_conf = self.slider.value()
