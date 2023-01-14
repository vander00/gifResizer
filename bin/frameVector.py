import os
import pickle


class FrameVector:
    def __init__(self, maxsize=1000):
        if isinstance(maxsize, int):
            self._maxsize = maxsize
        else:
            raise ValueError(f"MaxSize parameter must be integer (int), not {type(maxsize)}")
        self._framelist = list()  # List for _maxsize frames
        self._framescount = 0  # Counting all frames, not only in the list
        self._listsnumber = 0  # Counting all lists saved as files

    # Deleting all files created to save frames outside RAM
    def __del__(self):
        for number in range(self._listsnumber + 1):
            if os.path.exists(f"frames{number}"):
                os.remove(f"frames{number}")

    def append(self, *frames):
        for frame in frames:
            # If the list is too large, it copies into a file and the objects gets cleared
            if len(self._framelist) == self._maxsize:
                with open(f"frames{self._listsnumber}", "wb") as file:
                    pickle.dump(self._framelist, file)
                self._listsnumber += 1
                self._framelist.clear()
            self._framescount += 1
            self._framelist.append(frame)

    def __iter__(self):
        self._currentframe = 0

        return self

    def __next__(self):
        if self._currentframe < self._framescount:
            # Checking if the frame is in the list or in a file
            if self._currentframe >= self._maxsize * int((self._framescount - 1) / self._maxsize):
                self._currentframe += 1

                return self._framelist[self._currentframe - self._maxsize * int(self._currentframe / self._maxsize) - 1]
            else:  # If the file in the list, then load the list and return the item from one
                with open(f"frames{int(self._currentframe / self._maxsize)}", "rb") as file:
                    self._currentframe += 1

                    return pickle.load(file)[self._currentframe - self._maxsize * int(self._currentframe /
                                                                                      self._maxsize) - 1]
        else:
            raise StopIteration

    def __len__(self) -> int:
        return self._framescount

    def __getitem__(self, item):
        if isinstance(item, int):  # Checking if the item is integer
            # Checking if the item belongs to the list
            if -self._framescount <= item <= self._framescount:
                if item >= self._maxsize * int((self._framescount - 1) / self._maxsize):
                    return self._framelist[item - self._maxsize * int(item / self._maxsize)]
                else:
                    with open(f"frames{int(item / self._maxsize)}", "rb") as file:
                        return pickle.load(file)[item - self._maxsize * int(item / self._maxsize)]
            else:
                raise IndexError("Out of range.")
        else:
            raise TypeError(f"The index is invalid. It must be integer (int), not {type(item)}")
