import logging
import time

from droneapp.models.base import Singleton


logger = logging.getLogger(__name__)


class BaseCourse(metaclass=Singleton):

    def __init__(self, name, drone):
        self.name = name
        self.status = 0
        self.is_running = False
        self.start_time = None
        self.elapsed = None
        self.drone = drone

    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def stop(self):
        if not self.is_running:
            return False
        self.is_running = False
        self.status = 0

    def update_elapsed(self):
        if not self.is_running:
            return None
        self.elapsed = time.time() - self.start_time
        return self.elapsed

    def _run(self):
        raise NotImplementedError

    def run(self):
        if not self.is_running:
            return False
        self.status += 1
        self._run()
        self.update_elapsed()


class CourseA(BaseCourse):

    def _run(self):
        if self.status == 1:
            self.drone.takeoff()

        if (self.status == 10 or self.status == 15 or
                self.status == 20 or self.status == 25):
            self.drone.clockwise(90)

        if self.status == 30:
            self.drone.flip_front()

        if self.status == 40:
            self.drone.flip_back()

        if self.status == 50:
            self.drone.land()
            self.stop()


class CourseB(BaseCourse):

    def _run(self):
        if self.status == 1:
            self.drone.takeoff()

        if self.status == 10:
            self.drone.flip_front()

        if self.status == 20:
            self.drone.flip_back()
            if self.elapsed and 10 < self.elapsed < 15:
                self.status = 45

        if self.status == 30:
            self.drone.flip_right()

        if self.status == 40:
            self.drone.flip_left()

        if self.status == 50:
            self.drone.land()
            self.stop()


def get_courses(drone):
    return {
        1: CourseA('Course A', drone),
        2: CourseB('Course B', drone),
    }
