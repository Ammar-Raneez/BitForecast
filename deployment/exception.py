import sys

from logger import logging

def error_message_detail(error, detail):
  '''
  Create a custom detailed error message that can be used as a log
  '''

  _,_,exc_tb = detail.exc_info()
  file_name = exc_tb.tb_frame.f_code.co_filename
  error_message = 'Error occured in python script name [{0}] line number [{1}] error message[{2}]'.format(
    file_name, exc_tb.tb_lineno, str(error)
  )

  return error_message

class CustomException(Exception):
  def __init__(self, error_message, detail):
    super().__init__(error_message)
    self.error_message = error_message_detail(
      error_message,
      detail=detail
    )

  def __str__(self):
    return self.error_message

if __name__ == '__main__':
  try:
    val = 100 / 0
  except Exception as e:
    logging.info('Divide by zero')
    raise CustomException(e, sys)
