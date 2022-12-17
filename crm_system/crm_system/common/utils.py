from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile


def string_contains_only_letters(string: str) -> bool:
    """
    Checks if string contains only letters.

    :return: bool
    """
    return string.isalpha()


def calculate_years_between_dates(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    Calculates years between two dates.

    :return: int
    """
    return end_date.year - start_date.year - ((end_date.month, end_date.day) < (start_date.month, start_date.day))


def image_size_is_valid(image: InMemoryUploadedFile, max_size_in_mb: int) -> bool:
    """
    Validates if the size of the image is not more than the max allowed size.

    :return: bool
    """
    return image.size <= (max_size_in_mb * 1024 * 1024)
