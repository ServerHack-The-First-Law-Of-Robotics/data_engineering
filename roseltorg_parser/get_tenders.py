from parser import TenderParser
from config import mapping

TenderParser().go_through_pages(mapping['metal'], 'metal_tenders.txt')
TenderParser().go_through_pages(mapping['metal'], 'rubber_tenders.txt')
