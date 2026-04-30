import logging
import os
import shutil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

PUBLIC_PATH = "./public"
STATIC_PATH = "./static"


def main():
    logger.info("Clearing public directory")
    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)

    logger.info("Copying Static files and directories to Public.")
    copy_source_files(STATIC_PATH, PUBLIC_PATH)


def copy_source_files(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    logger.info(f"Entering Directory: {source_dir_path}")
    for item in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)
        logger.info(f"Copying: {source_path} -> {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_source_files(source_path, dest_path)


if __name__ == "__main__":
    main()
