import logging
import os

# DEFAULT LOG FORMATTER
_default_format_str = '%(asctime)s | %(levelname)s:%(name)s: %(message)s'
_default_date_fmt = '%m/%d/%Y %I:%M:%S %p'


def setup_logger(name, log_file, level=logging.INFO, log_format=_default_format_str, log_datefmt=_default_date_fmt):
    """
    Allows setting up multiple loggers with multiple types of formats, if needed.

    Example use:

    first_logger = setup_logger("first_logger", "first_logger.log", level=logging.DEBUG, log_format='%(asctime)s %(levelname)s %(message)s', log_datefmt='%m/%d/%Y %I:%M:%S %p')
    second_logger = setup_logger("second_logger", "second_logger.log", level=logging.INFO)

    first_logger.debug("Logging to first_logger")
    second_logger.info("Logging to second_logger")

    :param name: Name of the logger (Can use __name__ for name of file, or name of python log library such as 'werzeug' from Flask).
    :param log_file: filename of logger to print to (Must provide full path).
    :param level: Log level.
    :param log_format: The format used
    :param log_datefmt:
    :return:
    """
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(log_format, log_datefmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def delete_logger(log_file, logger):
    """

    :param log_file: Filepath of log file
    :param logger: Logger instance that needs to be deleted
    :return: None
    """
    # handler = logging.FileHandler(log_file)
    # logger.removeHandler(handler)
    for handler in logger.handlers:
        logger.removeHandler(handler)
    try:
        os.remove(log_file)
    except Exception as e:
        print(e)


def folder_exists(folder_path):
    """To check if a folder exists"""
    return os.path.isdir(folder_path)


# class TextHandler(logging.Handler):
#     """This class allows you to log to a Tkinter Text or ScrolledText widget"""
#
#     def __init__(self, text):
#         # run the regular Handler __init__
#         logging.Handler.__init__(self)
#         # Store a reference to the Text it will log to
#         self.text = text
#         self.text.config(state=DISABLED)
#
#     def emit(self, record):
#         msg = self.format(record)
#
#         def append():
#             self.text.configure(state=NORMAL)
#             self.text.insert(END, msg + '\n')
#             self.text.configure(state=DISABLED)
#             # Autoscroll to the bottom
#             self.text.yview(END)
#
#         # This is necessary because we can't modify the Text from other threads
#         self.text.after(0, append)


if __name__ == '__main__':
    first_logger = setup_logger('first_logger', os.path.join(os.getcwd(), 'first_logger.log'))
    second_logger = setup_logger('second_logger', os.path.join(os.getcwd(), 'second_logger.log'))

    first_logger.debug("Logging to first_logger")
    second_logger.info("Logging to second_logger")

