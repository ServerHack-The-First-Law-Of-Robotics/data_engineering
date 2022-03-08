from parser import TenderParser
import json
import time

tender_parser = TenderParser()

print(tender_parser.get_tender_page('/past/procedure/0877100000118000082'))