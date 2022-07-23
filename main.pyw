import os
import sched
import time
import paths  # absolute paths, change below as necessary


def scandir(s, base_directory: str, target_directory: str, extensions: tuple):
    s.enter(7, 1, scandir, argument=(s, base_directory, target_directory, extensions))
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


if __name__ == '__main__':
    main_path = paths.main_path  # directory that will be scanned for files

    images_path = paths.images_path  # the directory images are sorted into
    image_extensions = (".png", ".jpg", ".jpeg", ".jif", ".jfif", ".pjpeg", ".jfi", ".jpe", ".pjp", ".svg", ".svgz",
                        ".webp", ".ico", ".tif", ".tiff", ".bmp", ".apng", ".avif", ".heif", ".heic", ".eps", ".ai",
                        ".psd", ".gif")
    makedir(images_path)

    videos_path = paths.videos_path  # the directory videos are sorted into
    video_extensions = (".webm", ".mkv", ".flv", ".vob", ".ogg", ".ogv", ".avi", ".MTS", ".M2TS", ".TS", ".mov", ".qt",
                        ".wmv", ".amv", ".mp4", ".m4p", ".m4v", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v")
    makedir(videos_path)

    scheduler = sched.scheduler(time.time, time.sleep)
    schedule_scandir(scheduler, main_path, images_path, image_extensions)
    schedule_scandir(scheduler, main_path, videos_path, video_extensions)
    scheduler.run()
