from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QLineEdit, QGraphicsRectItem
from PyQt5 import QtGui, QtCore
import os

from utils.annotation import Annotation


class AnnotateWindow(QWidget):
    """
    This class acts a window where user is able to annotate images. Images must be located at the path found in GUI's "image_path_not_annotated" variable.
    This widget tracks all the mouse clicks and movements to determine where should the annotations be drawn.
    After user click the change image button this class uses Annotation classes save function to save all the new annnotations to the database.
    """
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.curr_image_clean = QLabel() # This holds image and all the previously drawn annotations. 
        self.curr_image_tmp = QLabel() # This hold all the data on the curr_image_clean + annotation under drawing
        self.curr_image_path = "" # Path of image currently shown
        self.begin = QtCore.QPoint() # Begin point of annotation currently under drawing
        self.end = QtCore.QPoint() # End point of annotation currently under drawing
        self.annotations_of_img = []  # List of Annotation objects drawn on the image
        self.layout = QGridLayout(self)
    
        self.init_widget()

    def paintEvent(self, event):
        """
        Draw the annotation and the image
        """
        # Make sure that curr_image contain image and thus there are images left to annotate
        # For some reason this function is called all the time so with this boolean logic we are able to prevent drawing happening all the time
        # We only want to draw when new_image button is clicked
        if not self.curr_image_tmp.pixmap().isNull() and self.drawing:
            self.curr_image_tmp.setPixmap(self.curr_image_clean.pixmap())
            tmp = QtGui.QImage(self.curr_image_tmp.pixmap().toImage());
            qp = QtGui.QPainter(tmp)
            br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 5))  
            qp.setBrush(br)
            qp.setPen(QtGui.QColor(255,255,0));
            
            # This makes sure that rect drawn on the last img is not show on the next one
            if self.begin != None:
                # Make sure we have a object written and the annotation is not just a dot
                if self.end != self.begin and self.text_box.text() != "":
                    # Make sure the annotation is inside the image
                    if 0 <= self.begin.x() <= self.gui.image_width and 0 <= self.begin.y() <= self.gui.image_height and 0 <= self.end.x() <= self.gui.image_width and 0 <= self.end.y() <= self.gui.image_height:
                        qp.drawRect(QtCore.QRect(self.begin, self.end))
                        if self.text_box.text() != "":
                            qp.drawText(self.begin.x(), self.begin.y(), self.text_box.text())
                    else:
                        print("Annotation must be inside the imgage")
                else:
                    print("Annotation must have an object and can not be a dot")
                    
            qp.end()
            # Update the pixmap to contain the new rect
            self.curr_image_tmp.setPixmap(QtGui.QPixmap.fromImage(tmp))
            self.drawing = False
        

    # --  Functions which hanlde the drawing of the annotations ---
    def mousePressEvent(self, event):
        c = self.modify_coordinates(event)
        self.begin = c
        self.end = c
        self.drawing = True
        self.update()

    def mouseMoveEvent(self, event):
        c = self.modify_coordinates(event)
        self.end = c
        self.drawing = True
        self.update()

    def mouseReleaseEvent(self, event):
        c = self.modify_coordinates(event)
        self.drawing = False
        self.end = c

        # Here create new annotation object and populate the annotations list.
        if self.end != self.begin and self.text_box.text() != "" and 0 <= self.begin.x() <= self.gui.image_width and 0 <= self.begin.y() <= self.gui.image_height and 0 <= self.end.x() <= self.gui.image_width and 0 <= self.end.y() <= self.gui.image_height:
            self.annotations_of_img.append(Annotation(self.begin, self.end, self.curr_image_path, self.text_box.text()))
        
        self.curr_image_clean.setPixmap( self.curr_image_tmp.pixmap())
        self.update()
    # -------------

    def modify_coordinates(self, event):
        """
        Coordinates in event parameter are associated with the pixelmap
        With this function the coordinates are modified so the coordinates match the actual location of mouse
        """
        c = event.pos()
        c.setX(event.pos().x() - self.curr_image_tmp.x())
        c.setY(event.pos().y() - self.curr_image_tmp.y())
        return c


    def new_image(self):
        """
        Function for the next image button
        Handles saving the annotations and showing new image
        """

        # Check if there is any annotations for current image and save them
        if self.annotations_of_img:
            for annotation in self.annotations_of_img:
                try:
                    annotation.save(self.gui.db)
                except Exception as e:
                    print(e)

            # Move the current image to annotated folder
            os.rename(self.gui.image_path_not_annotated  + self.curr_image_path, self.gui.image_path_annotated  + self.curr_image_path)
            # Empty the annotations folder
            self.annotations_of_img = []

        # Get new image
        self.curr_image_path = ""
        for filename in os.listdir(self.gui.image_path_not_annotated):
            # We might need to support more image types
            if filename.endswith(".png") or filename.endswith(".jpg"):
                self.curr_image_path = filename
                pixmap = QtGui.QPixmap(self.gui.image_path_not_annotated + self.curr_image_path).scaled(self.gui.image_width, self.gui.image_height)
                break

        # If no images left, show empty pixmap
        if self.curr_image_path == "":
            pixmap = QtGui.QPixmap()
        
        # This makes sure that rect drawn on the last img is not show on the next one
        self.begin, self.end = None, None
        self.curr_image_clean.setPixmap(pixmap)
        self.curr_image_tmp.setPixmap(pixmap)
        self.drawing = True
        self.update()

    def start_over(self):
        self.annotations_of_img = []
        pixmap = QtGui.QPixmap(self.gui.image_path_not_annotated + self.curr_image_path).scaled(self.gui.image_width, self.gui.image_height)
        self.begin, self.end = None, None
        self.curr_image_clean.setPixmap(pixmap)
        self.curr_image_tmp.setPixmap(pixmap)
        self.update()

    def init_widget(self):
        """
        Init all the components of the annotation window
        """ 

        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(100)

        # Input box of annotation object
        self.text_box = QLineEdit()
        
        # Initializing of different buttons
        self.change_image_btn = QPushButton("Change Image")
        self.start_over_btn = QPushButton("Clear Annotations")
        self.back_to_menu_btn = QPushButton("Back to Menu")

        self.change_image_btn.clicked.connect(self.new_image)
        self.start_over_btn.clicked.connect(self.start_over)
        self.back_to_menu_btn.clicked.connect(self.gui.init_window)

        # Get new image
        self.new_image()

        self.layout.addWidget(self.change_image_btn, 0, 1)
        self.layout.addWidget(self.start_over_btn, 0, 2)
        self.layout.addWidget(self.back_to_menu_btn, 0, 3)
        self.layout.addWidget(self.text_box, 0 , 0,)
        self.layout.addWidget(self.curr_image_tmp, 1, 0, 1, 0)

