import requests
import sys
import logging.config

from requests.exceptions import ConnectionError
from abc import ABCMeta, abstractmethod

from settings import logger_config


logging.config.dictConfig(logger_config)
logger = logging.getLogger('ResponseParser_logger')


class ResponseParser:
    def __init__(self, url):
        logger.info(' --- start response analysis ---')

        self._url = url
        self.response = self._get_response()

        self._parse()

    def _get_response(self):
        try:
            return requests.get(self._url)
        except ConnectionError:
            logger.critical('The page is not available!')
            sys.exit(1)

    def _parse(self):
        handlers = (StatusCodeHandler, CSPHandler)

        [handler(self.response) for handler in handlers]


class BaseHandler(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.handle(*args, **kwargs)

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass


class StatusCodeHandler(BaseHandler):
    def handle(self, response):
        status_code = response.status_code

        if status_code != 200:
            logger.warning('The response status code is {status_code}')


class CSPHandler(BaseHandler):
    def handle(self, response):
        headers = response.headers

        if 'Content-Security-Policy' not in headers:
            logger.info('CSP not detected')
        else:
            logger.info('CSP detected')