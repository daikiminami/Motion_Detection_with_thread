import cv2
from movie_img import MovieImg


class CapData:
    max_video_files = 1024 #static constexpr int
    max_filename_len = 1024 #static constexpr int
    # video_file_names[max_video_files][max_filename_len] #char
    # nvideo #int
    # #ringbuf_lock<imagebuf> *bufptr
    # frame_rate #fload //0: no fixed video rate == do not drop frame
    # loop_video #bool

    def __init__(self, vfile_size, vfiles, f=30.0, loop = False):
        self.nvideo = 0
        self.frame_rate = f
        self.loop_video = loop
        self.video_file_names = []
        print(vfiles[0])
        if vfile_size > 0:
            for i in range(vfile_size):
                if (vfiles[i] != None and vfiles[i][0] != None):
                    # self.video_file_names[i] = vfiles[:CapData.max_filename_len - 1] + self.video_file_names[nvideo][CapData.max_filename_len - 1:]
                    # self.video_file_names[i][CapData.max_filename_len - 1] = 0
                    self.video_file_names.append(vfiles[i])
                    self.nvideo += 1

    def cap_function(self, queue):
        n = self.nvideo
        print(n)
        if (n > 0):
            for i in range(n):
                f_name = self.video_file_names[i]
                cap_file = cv2.VideoCapture(f_name)
                if cap_file.isOpened() != True:
                    continue
                # アスペクト比の取得
                aspect_num = cap_file.get(cv2.CAP_PROP_SAR_NUM)
                aspect_den = cap_file.get(cv2.CAP_PROP_SAR_DEN)
                fno = 0
                while True:
                    ret, frame = cap_file.read()
                    if ret:
                        movie_img = MovieImg()
                        movie_img.set_attr(frame, fno = fno, aspect_num = aspect_num, aspect_den = aspect_den)
                        queue.put(movie_img)
                        fno += 1
                    else:
                        break





