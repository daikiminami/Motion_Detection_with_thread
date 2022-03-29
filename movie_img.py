class MovieImg:

    def __init__(self, img, fno = '', aspect_num = '', aspect_den = ''):
        self.w = img.shape[0]
        self.h = img.shape[1]
        self.ch = img.shape[2]
        self.fno = fno
        self.aspect_num = aspect_num
        self.aspect_num = aspect_den

    def set_attr(self, *attr):
        self.fno = attr[0]
        self.aspect_num = attr[1]
        self.aspect_num = attr[2]