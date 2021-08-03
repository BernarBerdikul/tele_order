from tele_order.utils import messages, constants
from tele_order.utils.exceptions import ValidationException
import re


def validate_image(image, max_image_size=constants.MAX_IMAGE_SIZE):
    if image.size > 1024 * 1024 * max_image_size:
        raise ValidationException({"image": messages.MAX_IMAGE_SIZE})


def validate_tag(value):
    if not re.match(constants.REGEX_FOR_FIRST_SYMBOL, value):
        raise ValidationException(
            detail={"tag": messages.FIRST_SYMBOL_VALIDATION})
    if not re.match(constants.REGEX_FOR_TAG, value):
        raise ValidationException(
            detail={"tag": messages.TAG_ANOTHER_SYMBOLS})
    if len(value) < constants.TAG_MIN_LENGTH:
        raise ValidationException(
            detail={"tag": messages.TAG_MIN_LENGTH})
    """ check value in reserved list of names """
    if value in constants.RESERVED_TAG_LIST:
        raise ValidationException(
            detail={"tag": messages.TAG_ALREADY_EXIST})
    return value.lower()
