from .sql_operations import create_annotation


class AnnotationException(Exception):
    """Exception raised for errors in the saving of annotation.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "".format(self.message)


class Annotation:
    """
    Class for annotations

    params:
        begin: QPoint object
        end: QPoint object
        image: string
        obj: string
    """
    def __init__(self, begin, end, image, obj):
        self.begin = begin
        self.end = end
        self.image = image
        self.obj = obj

    def save(self, db):
        """
        Function for saving the annotations to the database

        params:
            db: sqllite3 database connection object
        """
        # Here we want begin to be left top and end right bottom
        # But initially they can be in any corner
        xs = sorted([self.begin.x(), self.end.x()])
        ys = sorted([self.begin.y(), self.end.y()])
        coords = str((xs[0], ys[0], xs[1], ys[1]))
        annotation = (self.image, coords, self.obj)
        
        # Make sure coords are positive and the box is not a dot
        if all(flag >= 0 for flag in xs + ys) and (xs[0] != xs[1] and ys[0] != ys[1]):
            # Make sure correct filetype
            if self.image.endswith(".png") or self.image.endswith(".jpg") or self.image.endswith(".jpeg"):
                # Make sure there is a object
                if self.obj != "":
                    with db:
                        create_annotation(db, annotation)
                else:
                    raise AnnotationException("No object, not saved")
            else:
                raise AnnotationException("Unsupported file type, not saves")
        else:
            raise AnnotationException("Negative coordinates, not saved")
    