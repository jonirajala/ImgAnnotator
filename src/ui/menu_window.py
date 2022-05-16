import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5 import QtGui, QtCore
import os

from annotate_window import AnnotateWindow
from explore_annotations_window import ExploreAnnotationsWindow

class MenuWindow(QWidget):
    """
    This class acts a menu window. This window contains buttons for navigating to different parts of the program.
    
    """
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.layout = QGridLayout(self)

        self.init_menu()
        
    def annotate_window_btn_clicked(self):
        """
        Button for navigating to the annotate window
        """
        self.gui.curr_widget = AnnotateWindow(self.gui)
        self.gui.setCentralWidget(self.gui.curr_widget)

    def explore_annotations_btn_clicked(self):
        """
        Button for navigating to the explore annotations window
        """
        self.gui.curr_widget = ExploreAnnotationsWindow(self.gui)
        self.gui.setCentralWidget(self.gui.curr_widget)
        

    def init_menu(self):
        """
        Initializes all the buttons and texts
        """
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(100)

        # Set up font for the title
        font = QtGui.QFont()
        font.setPixelSize(30)
        font.setBold(True);

        self.title = QLabel();
        self.title.setText("Joni's sick annotation program")
        self.title.setFont(font)

        # Set up font for the subtitles
        font = QtGui.QFont()
        font.setPixelSize(15)
        font.setBold(True);

        images = []
        for filename in os.listdir(self.gui.image_path_not_annotated):
            # Here we might need more file types
            if (filename.endswith(".png") or filename.endswith(".jpg")):
                images.append(filename)

        self.images_left = QLabel();
        self.images_left.setText(f"Images left to annotate: {len(images)}")
        self.images_left.setFont(font)

        images = []
        for filename in os.listdir(self.gui.image_path_annotated):
            # Here we might need more file types
            if (filename.endswith(".png") or filename.endswith(".jpg")):
                images.append(filename)
        self.annotation_counter = QLabel();
        self.annotation_counter.setText(f"Images annotated: {len(images)}")
        self.annotation_counter.setFont(font)
        

        # Initilize buttons and connect them to the corresponding functions
        self.annotate_window_btn = QPushButton("Annotate")
        self.explore_annotations_btn = QPushButton("Explore Annotations")
        self.annotate_window_btn.clicked.connect(self.annotate_window_btn_clicked)
        self.explore_annotations_btn.clicked.connect(self.explore_annotations_btn_clicked)
        


        # Add buttons and titles to the layout
        self.layout.addWidget(self.title, 0, 0, 1, 0)
        self.layout.addWidget(self.annotate_window_btn, 1, 0)
        self.layout.addWidget(self.explore_annotations_btn, 1, 1)

        # Counter for annotated images
        self.layout.addWidget(self.images_left, 2, 0)

        # Counter for not_annotated images
        self.layout.addWidget(self.annotation_counter, 2, 1)
