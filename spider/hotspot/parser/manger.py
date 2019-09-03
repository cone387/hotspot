import os
import time
from .parser import Parser, logger
from .common import CommonParser
import importlib


class ParserManager(object):
    _parsers = {}   # [{id: '', 'object': '', 'name': ''}]
    _parser_modules = set()
    
    def __init__(self):
        super().__init__()
        self.load_parsers()

    def _load_parser_from(self, from_file):
        try:
            from_module = from_file.split('/')[-1].split('\\')[-1].split('.')[0]
            parser_module = importlib.import_module(f'hotspot.parser.special.{from_module}')
        except Exception as e:
            logger.info("Load error from %s:%s", from_file, str(e))
            return False
        for _, obj in parser_module.__dict__.items():
            if type(obj).__name__ == 'type' and issubclass(obj, Parser) \
                    and obj.__name__ not in (Parser.__name__, CommonParser.__name__):
                name = getattr(obj, 'name', None)
                if not name:
                    logger.info("%s must have board_id or site_id from %s", obj.__name__, from_file)
                    return False
                logger.info("Load %s from %s success", obj.__name__, from_file)
                self._parsers[name] = obj
                self._parser_modules.add(from_file)
                return True
        logger.info("No Parser subclass found from %s"%from_file)
        return False

    def reload_from(self, from_file):
        try:
            from_module = from_file.split('/')[-1].split('\\')[-1].split('.')[0]
            parser_module = importlib.import_module(f'hotspot.parser.special.{from_module}')
            parser_module = importlib.reload(parser_module)
            for _, obj in parser_module.__dict__.items():
                if type(obj).__name__ == 'type' and issubclass(obj, Parser) and obj.__base__ == Parser:
                    name = getattr(obj, 'name', None)
                    if not name:
                        logger.info("%s must have site name", obj.__name__)
                        return False
                    logger.info("Reload parser from %s success"%from_file)
                    self._parsers[name] = obj
                    self._parser_modules.add(from_file)
                    return True
            return False
        except Exception as e:
            logger.info("Reload error from %s:%s", from_file, str(e))
            return False

    def find_parser(self, config) -> Parser:
        parser = self._parsers.get(config.get('name'))
        if parser:
            return parser
        return CommonParser

    def load_parsers(self):
        parser_files = os.listdir('hotspot/parser/special')
        for parser_file in parser_files:
            if parser_file.startswith('_') or not parser_file.endswith('py'):
                continue
            if parser_file not in self._parser_modules:
                self._load_parser_from(parser_file)
        logger.info("%s special parser loaded"%len(self._parsers))
