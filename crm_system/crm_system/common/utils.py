import os
from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile


def string_contains_only_letters(string: str) -> bool:
    """
    Checks if string contains only letters.

    :return: bool
    """
    return string.isalpha()


def calculate_years_between_dates(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    Calculates year difference between two dates.

    :return: int
    """
    return end_date.year - start_date.year - ((end_date.month, end_date.day) < (start_date.month, start_date.day))


def image_size_is_valid(image: InMemoryUploadedFile, max_size_in_mb: int) -> bool:
    """
    Checks if the size of the image in MB is not greater than the allowed size.

    :return: bool
    """
    return image.size <= (max_size_in_mb * 1024 * 1024)


def create_image(name: str, path: str):
    """
    Creates a simple representation of a file, which has content and a name.

    :return: SimpleUploadedFile
    """
    return SimpleUploadedFile(name=name, content=open(path, 'rb').read())


def delete_file(path: str) -> None:
    """
    Deletes file by given path if exists.

    :return: None
    """

    if os.path.exists(path):
        os.remove(path)
