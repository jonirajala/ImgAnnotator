from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QLineEdit, QGraphicsRectItem
from PyQt5 import QtGui, QtCore
import os

from utils.annotation import Annotation
from utils.sql_operations import select_annotations_by_image_name


class ExploreAnnotationsWindow(QWidget):
    """
    This class acts a window where user is able to explore annotated images. Images must be located at the path found in GUI's "image_path_annotated" variable.
    For every image the class makes SQL query to the database to get all the annotations assocated with the current image and shows image and annotations.
    """
    def __init__(self, gui):
        super().__init__()
        self.curr_image_path = "" # Path of image currently shown
        self.annotations_of_curr_image = [] # List of annotations of current image
        self.layout = QGridLayout(self)
        self.gui = gui
        self.curr_image = QLabel() # This holds image and all the annotations. 
        self.images = [] # All the images containing annotations

        self.filter_images() # Gets all the images form the path and saves them to list
        self.init_widget()

    def paintEvent(self, event):
        """
        Draw the annotation and the image
        """
        # For some reason this function is called all the time so with this boolean logic we are able to prevent drawing happening all the time
        # We only want to draw when new_image button is clicked and pixmap is not null
        if self.draw and not self.curr_image.pixmap().isNull():
            tmp = QtGui.QImage(self.curr_image.pixmap().toImage());
            qp = QtGui.QPainter(tmp)
            br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 0))  
            qp.setBrush(br)
            qp.setPen(QtGui.QColor(255,255,0));
            
            for annotation in self.annotations_of_curr_image:
                qp.drawRect(QtCore.QRect(annotation.begin, annotation.end))
                qp.drawText(annotation.begin.x(), annotation.begin.y(), annotation.obj)

            self.curr_image.setPixmap(QtGui.QPixmap.fromImage(tmp))

            qp.end()
            self.draw = False       

    def new_image(self):
        """
        Function for the next image button
        Queries all the annotations for next image
        """

        # Take the first image of list and move it to the back of the list
        if len(self.images) > 0:
            self.curr_image_path = self.images[0]
            self.images.append(self.images.pop(0))

        # Draw the image
        pixmap = QtGui.QPixmap(self.gui.image_path_annotated + self.curr_image_path).scaled(self.gui.image_width, self.gui.image_height)
        self.curr_image.setPixmap(pixmap)
        # Make SQL query to get all the annotations for this image and make annotion objects
        self.annotations_of_curr_image = []
        annotations = select_annotations_by_image_name(self.gui.db, self.curr_image_path)
        for annotation in annotations:
            # annotation is in format: (id, image, annotation, class)
            # annotation: self.begin.x(), self.begin.y(), self.end.x(), self.end.y()
            coords = (annotation[2][1:-1]).split(", ")
            begin = QtCore.QPoint(int(coords[0]), int(coords[1]))
            end = QtCore.QPoint(int(coords[2]), int(coords[3]))
            self.annotations_of_curr_image.append(Annotation(begin, end, annotation[1], annotation[3]))
        self.draw = True
        self.update()

    def filter_images(self):
        """
        Take all the images of the folder and filter only image files
        """
        for filename in os.listdir(self.gui.image_path_annotated):
            # Here we might need more file types
            if (filename.endswith(".png") or filename.endswith(".jpg")):
                self.images.append(filename)

    def init_widget(self):
        """
        Init all the components of the explore annotation window
        """ 

        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(100)

        # Initializing of different buttons
        self.change_image_btn = QPushButton("Change Image")
        self.back_to_menu_btn = QPushButton("Back to Menu")

        self.change_image_btn.clicked.connect(self.new_image)
        self.back_to_menu_btn.clicked.connect(self.gui.init_window)
        
        # Get new image
        self.new_image()

        self.layout.addWidget(self.change_image_btn, 0, 0)
        self.layout.addWidget(self.back_to_menu_btn, 0, 1)
        self.layout.addWidget(self.curr_image, 1, 0, 1, 0)