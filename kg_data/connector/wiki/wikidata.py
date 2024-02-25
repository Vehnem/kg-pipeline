class WikidataAdapter:
    """
    Adapter for Wikidata.
    """

    def getExternalIdsForType(self, type):
        """
        Returns a list of external ids for a given type.
        """
        return self.datasource.getExternalIdsForType(type)
    
    def getExtenalIdsForEntity(self, entity):
        """
        Returns a list of external ids for a given entity.
        """
        return self.datasource.getExternalIdsForEntity(entity)