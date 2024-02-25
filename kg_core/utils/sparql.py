
from SPARQLWrapper import SPARQLWrapper, JSON

def fetch_all_sparql_data(endpoint, limit, query):
    """
    Queries the given SPARQL endpoint in a loop to fetch all data, 
    avoiding the endpoint's return limit.

    :param endpoint: The SPARQL endpoint URL.
    :param limit: The maximum number of results the endpoint can return in a single query.
    :param query: The SPARQL query to execute.
    :return: A list containing all the results.
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)

    offset = 0
    results_aggregated = []

    while True:
        # Append the LIMIT and OFFSET to the query
        modified_query = query + f" LIMIT {limit} OFFSET {offset}"
        sparql.setQuery(modified_query)
        
        # Query the endpoint
        results = sparql.query().convert()
        results = results["results"]["bindings"]
        
        # If no results are returned, we've reached the end
        if not results:
            break
        
        # Add the results to the aggregated list
        results_aggregated.extend(results)
        
        # Increase the offset for the next iteration
        offset += limit

    return results_aggregated
