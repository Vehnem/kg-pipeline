###Processing imdb dataset###

import csv

from llm4kg_dataset.acquisition.data_source_adapter import DataSourceAdapter

class ImdbAdapter(DataSourceAdapter):
    """Adapter for imdb dataset"""

    def convert_to_rdf(self, csv_file_path, rdf_file_path):
        """Converts the imdb dataset from csv to rdf
        Example of csv file:
        nconst,primaryName,birthYear,deathYear,primaryProfession,knownForTitles
        Example of rdf file:
        <http://example.org/resource/1> <http://example.org/property/primaryName> "Fred Astaire" .
        """
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            with open(rdf_file_path, "w") as rdf_file:
                for row in csv_reader:
                    rdf_file.write(
                        "<http://example.org/resource/"
                        + row["nconst"]
                        + "> <http://example.org/property/primaryName> "
                        + '"'
                        + row["primaryName"]
                        + '"'
                        + " .\n"
                    )
        