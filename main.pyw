import os
import sched
import time


def scandir(s, base_directory: str, target_directory: str, extensions: tuple):
    s.enter(5, 1, scandir, argument=(s, base_directory, target_directory, extensions))
    print("Scanning directory "+base_directory+" and moving files to "+target_directory)
    for entry in os.listdir(base_directory):
        entry_base_path = os.path.join(base_directory, entry)
        if not os.path.isfile(os.path.join(base_directory, entry)):
            continue
        if entry.lower().endswith(extensions):
            i = 0
            while True:
                name = entry if i == 0 else " ({})".format(i).join(os.path.splitext(entry))
                print(name)
                entry_target_path = os.path.join(target_directory, name)
                if not os.path.exists(entry_target_path):
                    os.rename(entry_base_path, entry_target_path)
                    break
                i += 1


def makedir(*pathname):
    path = "C:/"
    if pathname.__len__() == 1:
        path = pathname[0]
    if pathname.__len__() == 2:
        path = os.path.join(pathname[0], pathname[1])
    if pathname.__len__() > 2:
        raise Exception("Too many arguments supplied")
    if os.path.isdir(path):
        return
    os.mkdir(path)
    return path


def schedule_scandir(s, base_directory: str, target_directory: str, extensions: tuple):
    print(time.ctime())
    s.enter(7, 1, scandir, argument=(s, base_directory, target_directory, extensions))
    s.run()


if __name__ == '__main__':
    main_path = "C:/Users/kunal/Downloads/"  # directory that will be scanned
    images_path = "C:/Users/kunal/Downloads/Images/"
    image_extensions = (".png", ".jpg", ".jpeg", ".jif", ".jfif", ".pjpeg", ".jfi", ".jpe", ".pjp", ".svg", ".svgz",
                        ".webp", ".ico", ".tif", ".tiff", ".bmp", ".apng", ".avif", ".heif", ".heic", ".eps", ".ai",
                        ".psd")
    makedir(images_path)

    scheduler = sched.scheduler(time.time, time.sleep)
    schedule_scandir(scheduler, main_path, images_path, image_extensions)
