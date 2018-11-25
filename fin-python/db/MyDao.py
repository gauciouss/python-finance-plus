import abc

class MyDaoTemplate(metaclass=abc.ABCMeta):
    
    session_factory = None
    logger = None

    def doSearch(self):
        return None