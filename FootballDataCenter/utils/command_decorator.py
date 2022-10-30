import traceback
from multiprocessing.context import Process

from django.conf import settings
from numpy.ma.bench import timer
import logging


def command_decorator(logger_obj, custom_msg=''):
    if not logger_obj:
        raise Exception('logging object not defined, is None')

    if not isinstance(logger_obj, logging.Logger):
        raise Exception('Bad logger object passed')

    def real_decorator(function):
        def wrapped_function(*func_args, **func_kargs):
            p = Process()
            p.name = custom_msg
            p.start()

            logger_obj.debug(' {} function args: {}'.format(custom_msg,
                                                            str(func_args)))
            logger_obj.info('Starting {} ...' .format(custom_msg))

            v = None
            start = timer()
            try:
                v = function(*func_args, **func_kargs)
                spent = timer() - start
                logger_obj.info('{} finished!'.format(custom_msg))
            except Exception as e:
                logger_obj.error(e)
                logger_obj.error(traceback.format_exc())
                spent = timer() - start
                p.error_status()
                message = 'Error in command {} . Exception \n{}\n{}'.format(
                    custom_msg, repr(e), traceback.format_exc()
                )
            else:
                p.ok_status()
            finally:
                message = 'Spent {} seconds executing {}'.format(spent,
                                                                 custom_msg)
                logger_obj.info(message)
                return v

        return wrapped_function
    return real_decorator
