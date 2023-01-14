import os
from urllib.request import urlopen

from PIL import Image, GifImagePlugin

from frameVector import FrameVector

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS


class Gif:
    # "Exists" means if the file exists, or it needs being made
    def __init__(self, path):
        # The path might be to HTTP URL or just to a local directory on a computer
        self.path = path

        # Checking if the path is a URL or a local path of the computer
        if self.path.split(":")[0] == "https" or self.path.split(":")[0] == "http":
            self.image = Image.open(urlopen(self.path))
        elif not os.path.exists(self.path):
            self.image = Image.new("RGBA", (126, 90))
            self.image.seek(0)
        else:
            self.image = Image.open(self.path)

    # Saving a gif file with all frames from the buffer
    def close(self, buffer):
        self.image.save(self.path, save_all=True, append_images=buffer, loop=0, include_color_table=True)

    # Returning the current frame we are on of the gif
    def getcurrentframe(self) -> Image:
        return self.image.crop()  # Returning the current frame we have selected

    def movetonextframe(self):
        try:
            self.image.seek(self.image.tell() + 1)  # Moving to the next frame by one
        except EOFError:
            self.image.seek(0)

    # Getting a number of all frames
    def getframes(self) -> int:
        return self.image.n_frames


#  Returning a size of a frame in bytes
def getsizeofimage(image) -> int:
    image.save("oneframe__.gif")

    filesize = os.path.getsize("oneframe__.gif")

    image.close()
    os.remove("oneframe__.gif")

    return filesize


def take_frames_from(imagepath, buffer, desiredsize):
    source = Gif(imagepath)
    # Calculating how many frames we need the output file to be "desiredsize" bytes
    repeats = int(desiredsize / (getsizeofimage(source.getcurrentframe()) - 500))

    for time in range(repeats):
        buffer.append(source.getcurrentframe())
        source.movetonextframe()


def put_frame_to(imagepath, buffer):
    # Checking if the path is a URL or a local path of the computer
    # Making a large gif in the folder of the script if the path is url or
    # in the folder where the smaller gif is
    if imagepath.split(":")[0] == "https" or imagepath.split(":")[0] == "http":
        destination = Gif("larger.gif")
    else:
        if os.path.exists(str(imagepath.split(".")[0]) + "_large.gif"):
            os.remove(str(imagepath.split(".")[0]) + "_large.gif")
        destination = Gif(imagepath.split(".")[0] + "_large.gif")

    destination.close(buffer)


if __name__ == "__main__":

    sizeoffile = None
    frames = None

    while True:
        try:
            # List to save all frames from the gif
            frames = FrameVector(int(input("Enter a number of length of a buffer of frames: ")))
            break
        except ValueError:
            print("Error! You've entered a wrong number.")

    while True:
        while True:
            filepath = input("\nEnter an URL/Full local file path to a gif (1000 is default): ")
            if filepath.split(":")[0] != "https" and filepath.split(":") != "http" and os.path.exists(filepath):
                break
            print("Error: You've entered a wrong path, the file does not exist.")
        while True:
            try:
                sizeoffile = input("\nEnter the final size of the gif should be (KiloBytes): ")
                if sizeoffile.lower() == "back":
                    break
                if int(sizeoffile) * 1000 < os.path.getsize(filepath):
                    print("Error! The size is less than the original file's size!")
            except ValueError:
                print("Error: You've entered a wrong number!")
                continue
            sizeoffile = int(sizeoffile)
            break
        if sizeoffile != "back":
            break

    take_frames_from(filepath, frames, sizeoffile * 1000)  # Size * 1000 turn the size into bytes
    put_frame_to(filepath, frames)
