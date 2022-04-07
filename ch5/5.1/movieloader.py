import os
import queue
import threading

import cv2

class MovieLoader:
    def __init__(self, src_path, max_queue_size=256):
        if type(src_path) == str and (not os.path.exists(src_path)):
            raise FileNotFoundError(f'No such file {src_path}')

        self.video = cv2.VideoCapture(src_path)
        self.stopped = False
        self._q = queue.Queue(maxsize=max_queue_size)

        self._thread = threading.Thread(target=self.update, daemon=True)
        self._thread.start()


    def update(self):
        while True:
            if self.stopped:
                break

            if not self.video.isOpened():
                break

            if self.pos_frames >= self.frame_count and self.frame_count > 0:
                break

            if not self._q.full():
                ok, frame = self.video.read()

                if (not ok) or (frame is None):
                    continue
                else:
                    self._q.put(frame)

        self.stopped = True


    def read(self, block=True, timeout=None):
        return self._q.get(block, timeout)

    def stop(self):
        self.stopped = True

    def release(self):
        self.stopped = True
        self.video.release()

    def isOpened(self):
        return self.video.isOpened()

    def get(self, key):
        return self.video.get(key)

    def set(self, key, value):
        return self.video.set(key, value)

    @property
    def frame_width(self):
        return int(self.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def frame_height(self):
        return int(self.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def frame_count(self):
        return self.get(cv2.CAP_PROP_FRAME_COUNT)

    @property
    def fps(self):
        return self.get(cv2.CAP_PROP_FPS)

    @property
    def pos_msec(self):
        return self.get(cv2.CAP_PROP_POS_MSEC)

    @property
    def pos_frames(self):
        return self.get(cv2.CAP_PROP_POS_FRAMES)


if __name__ == '__main__':

    cap = MovieLoader('test.mp4')
    #cap = MovieLoader(0) # Webカメラからの読み取り

    while not cap.stopped:
        frame = cap.read(timeout=1)

        cv2.putText(frame,
                f'{int(cap.pos_frames)}/{int(cap.frame_count)}',
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                thickness=2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27: # ESCキーで終了
            break

