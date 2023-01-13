from PIL import Image, GifImagePlugin
from urllib.request import urlopen
import os

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS


class Gif:
    # "Exists" means if the file exists, or it needs being made
    def __init__(self, path):
        # The path might be to HTTP URL or just to a local directory on a computer
        self.path = path
        if self.path.split(":")[0] == "https" or self.path.split(":")[0] == "http":
            self.image = Image.open(urlopen(self.path))
            self.framesnumber = self.image.n_frames

        elif not os.path.exists(self.path):
            self.image = Image.new("RGBA", (126, 90))
            self.image.seek(0)
        else:
            self.image = Image.open(self.path)
            self.framesnumber = self.image.n_frames

    # Saves a gif file with all frames from the buffer
    def close(self, buffer):
        self.image.save(self.path, save_all=True, append_images=buffer, loop=0)

    # Returns the current frame we are on of the gif
    def currentframe(self) -> Image:
        if self.image.tell() >= self.framesnumber:
            self.__init__(self.path)

        currentframe = self.image
        self.image.seek(self.image.tell() + 1)  # Move to the next frame by one

        return currentframe


def take_frames_from(imagepath, buffer, desiredsize):
    source = Gif(imagepath)
    repeats = int(desiredsize / (os.path.getsize(imagepath) / source.framesnumber))

    for time in range(repeats):  # Gets
        buffer.append(source.currentframe())


def put_frame_to(imagepath, buffer):
    if imagepath.split(":")[0] == "https" or imagepath.split(":")[0] == "http":
        destination = Gif("larger.gif")
    else:
        if os.path.exists(str(imagepath.split(".")[0]) + "_large.gif"):
            os.remove(str(imagepath.split(".")[0]) + "_large.gif")
        destination = Gif(imagepath.split(".")[0] + "_large.gif")

    destination.close(buffer)


if __name__ == "__main__":
    frames = list()  # Queue for exchanging frames between two processes
    size = None

    while True:
        while True:
            filepath = input("\nEnter an URL/Full local file path to a gif: ")
            if not (filepath.split(":")[0] != "https" and filepath.split(":") != "http" and os.path.exists(filepath)):
                print("Error: You've entered a wrong path, the file does not exist.")
                continue
            break
        while True:
            try:
                size = input("\nEnter the final size of the gif should be (KiloBytes): ")
                if size.lower() == "back":
                    break
                if int(size) * 1000 < os.path.getsize(filepath):
                    print("Error! The size is less than the original file's size!")
            except ValueError:
                print("Error: You've entered a wrong number!")
                continue
            size = int(size)
            break
        if size != "back":
            break

    take_frames_from(filepath, frames, size * 1000)  # Size * 1000 turn the size into bytes
    put_frame_to(filepath, frames)
