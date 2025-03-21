import sys
import os
from typing import List
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout, QPushButton, QFileSystemModel
from PyQt5.QtCore import Qt, QEvent


class DirectoryBrowser(QWidget):

    def __init__(self, title: str) -> None:
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.tree_view = QTreeView()
        self.tree_view.setSelectionMode(QTreeView.MultiSelection)
        self.model = QFileSystemModel()
        current_directory = os.getcwd()
        self.model.setRootPath(current_directory)

        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(current_directory))

        self.selected_items = []

        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.get_selected_items)

        self.layout.addWidget(self.tree_view)
        self.layout.addWidget(self.select_button)

        self.setLayout(self.layout)

        self.tree_view.setColumnWidth(0, 300)

        self.tree_view.installEventFilter(self)

    def get_selected_items(self) -> None:
        selected_indexes = self.tree_view.selectionModel().selectedIndexes()
        selected_items = {self.model.filePath(index) for index in selected_indexes}

        self.selected_items = self.recursive_selection(selected_items)
        self.close()

    def eventFilter(self, obj, event) -> bool:
        if obj is self.tree_view and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                self.get_selected_items()
        return super().eventFilter(obj, event)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            index = self.tree_view.currentIndex()
            if index.isValid():
                path = self.model.filePath(index)
                if os.path.isdir(path):
                    self.tree_view.setExpanded(index, not self.tree_view.isExpanded(index))
                else:
                    self.get_selected_items()

    def recursive_selection(self, paths: set) -> List[str]:
        selected_items = []
        for path in paths:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    selected_items.extend([os.path.join(root, f) for f in files + dirs])
            else:
                selected_items.append(path)
        return selected_items


def main(tab_name: str) -> List[str]:
    app = QApplication(sys.argv)
    window = DirectoryBrowser(tab_name)
    window.show()
    app.exec_()
    return window.selected_items


if __name__ == "__main__":
    selected_items = main("Your Tab Name")
    print("Selected Items:", selected_items)
