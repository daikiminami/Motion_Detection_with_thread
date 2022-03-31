class MovieImg:

    def __init__(self):
        self.img = ''
        self.w = ''
        self.h = ''
        self.ch = ''
        self.fno = ''
        self.aspect_num = ''
        self.aspect_num = ''

    def set_attr(self, img, fno = '', aspect_num = '', aspect_den = ''):
        self.img = img
        self.w = img.shape[1]
        self.h = img.shape[0]
        self.ch = img.shape[2]
        self.fno = fno
        self.aspect_num = aspect_num
        self.aspect_num = aspect_den
