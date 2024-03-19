#Evaluation metrics for the LLM4KG project

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from rdflib import Graph, Literal, URIRef
from rdflib.plugins.sparql import sparql
from kg_core.utils.annotation import todo
from kg_core.metrics.ontology import HiearchyBasedScores

# todo https://networkx.org/documentation/stable/reference/algorithms/similarity.html

with open("kg_tests/resources/llm4rml/rml-ontology_parsed.ttl", "r") as f:
    ONTOLOGY_DATA = f.read()

graph_onto = Graph().parse(data=ONTOLOGY_DATA, format="turtle")

idsByType = {
    'http://dbpedia.org/ontology/Film': [
        'tt0167423'
    ],
    'http://dbpedia.org/ontology/Person': [
        'nm0000002',
        'nm0000018',
        'nm0000101',
        'nm0002706',
        'nm0006107',
        'nm0021607',
        'nm0038875',
        'nm0254580',
        'nm0441631',
        'nm4500812'
    ],
    'http://dbpedia.org/ontology/Actor' : [
        'nm0000002',
        'nm0000018',
        'nm0000101',
        'nm0021607'
    ]
}

class Metrics:
    """
    Metrics to calulate the performance of the model
    - Accuracy
    - Precision
    - Recall
    - F1-score
    """

    def accuracy_score(self, y_true, y_pred):
        """
        Calculates the accuracy of the model

        How close a measurement or attempt is to the actual value or target

        """
        return accuracy_score(y_true, y_pred)
    

    def precision_score(self, y_true, y_pred):
        """
        Calculates the precision of the model
        How consistent the results are regardless of proximity to the actual value or target
        This is not needed for the LLM4KG project
        """
        return precision_score(y_true, y_pred)
    

    def recall_score(self, y_true, y_pred):
        """
        Calculates the recall of the model
        """
        return recall_score(y_true, y_pred)
    

    def f1_score(self, y_true, y_pred):
        """
        Calculates the f1-score of the model
        """
        return f1_score(y_true, y_pred)
    

class RDF_Similarity_Metrics:
    """
    Metrics to calulate the RDF similarity of the model
    """
    pass

    def __init__(self, test_graph: Graph, reference_graph: Graph) -> None:
        self.test_graph = test_graph
        self.reference_graph = reference_graph
        pass

    def precision_score(self):
        pass

    def recall_score(self):
        pass

    def f1_score(self):
        pass

def overlapping_lists(l1, l2):
    s1 = sorted(l1)
    s2 = sorted(l2)

    overalp = []

    i = 0
    j = 0
    while i < len(s1) and j < len(s2):
        if s1[i] < s2[j]:
            i += 1
        elif s1[i] > s2[j]:
            j += 1
        else:
            overalp.append(s1[i])
            i += 1
            j += 1
    return overalp


def precision_score(tp, fp):
    return tp / (tp + fp) if tp + fp > 0 else 0

def recall_score(tp, fn):
    return tp / (tp + fn) if tp + fn > 0 else 0

def f1_score(tp, fp, fn):
    precision = precision_score(tp, fp)
    recall = recall_score(tp, fn)
    return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0

RDF_TYPE_URI='http://www.w3.org/1999/02/22-rdf-syntax-ns#type'

class RML_Evaluation():
    """
    Metrics to calulate the scores for the RML evaluation
    """


    def __init__(self, test_graph: Graph, reference_graph: Graph) -> None:
        self.test_graph = test_graph
        self.reference_graph = reference_graph
        self.BASE_IRI = 'http://mykg.org/resource/'
        pass

    def subjects(self) -> dict:
        # number of predicted subjects (tp+fp+tn+fn)
        # number of expected subjects (tp+tn)
        # number of correct subjects (tp)
        # number of unexpected subjects (fp)

        test_graph_subjecIRIs = set([s for s, p, o in self.test_graph])
        reference_graph_subjectIRIs = set([s for s, p, o in self.reference_graph])

        tp = len(test_graph_subjecIRIs.intersection(reference_graph_subjectIRIs))
        fp = len(test_graph_subjecIRIs) - tp
        fn = len(reference_graph_subjectIRIs) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    @todo()
    def subjects_fuzzy(self) -> dict:

        test_graph_subjecIRIs = set([s for s, p, o in self.test_graph])
        reference_graph_subjectIRIs = set([s for s, p, o in self.reference_graph])
        reference_ids = [str(s).split("/")[-1] for s, p, o in self.reference_graph]

        tp = 0
        for s in test_graph_subjecIRIs:
            if any(id in s for id in reference_ids):
                tp += 1

        fp = len(test_graph_subjecIRIs) - tp
        fn = len(reference_graph_subjectIRIs) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}


    def tripleScore(self) -> dict:
        
        test_triples = set([s+p+o for s, p, o in self.test_graph])
        reference_triples = set([s+p+o for s, p, o in self.reference_graph])

        tp = len(test_triples.intersection(reference_triples))
        fp = len(test_triples) - tp
        fn = len(reference_triples) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    def classes_unique(self) -> dict:
        
        test_classes = set([o for s, p, o in self.test_graph if str(p) == RDF_TYPE_URI])
        reference_classes = set([o for s, p, o in self.reference_graph if str(p) == RDF_TYPE_URI])

        tp = len(test_classes.intersection(reference_classes))
        fp = len(test_classes) - tp
        fn = len(reference_classes) - tp
        tn = 0

        precision= precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return { 'test_classes': list(test_classes), 'reference_classes': list(reference_classes), 'precision': precision, 'recall': recall, 'f1': f1}

    def classes(self) -> dict:
        test_classes = list([o for s, p, o in self.test_graph if str(p) == RDF_TYPE_URI])
        reference_classes = list([o for s, p, o in self.reference_graph if str(p) == RDF_TYPE_URI])

        tp = len(overlapping_lists(test_classes, reference_classes))
        fp = len(test_classes) - tp
        fn = len(reference_classes) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_classes': list(test_classes), 'reference_classes': list(reference_classes), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    @todo("implement with sparl query")
    def properties_unique(self) -> dict:
        
        test_po = set([p+o for s, p, o in self.test_graph])
        reference_po = set([p+o for s, p, o in self.reference_graph])

        tp = len(test_po.intersection(reference_po))
        # unexpected 
        fp = len(test_po) - tp
        # missing
        fn = len(reference_po) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_po': list(test_po), 'reference_po': list(reference_po),'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}
    
    # @todo("implement with sparl query")
    def properties(self) -> dict:
        test_po = list([p for s, p, o in self.test_graph])
        reference_po = list([p for s, p, o in self.reference_graph])

        tp = len(overlapping_lists(test_po,reference_po))
        fp = len(test_po) - tp
        fn = len(reference_po) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'f1': f1, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

        # return {'test_po': list(test_po), 'reference_po': list(reference_po), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    # def unique_property_datatype_score(self) -> dict:

    #     test_p_o_datatypes = set([str(p)+' '+str(o.datatype if isinstance(o, Literal) else '') for s, p, o in self.test_graph])
    #     reference_p_o_datatypes = set([str(p)+' '+str(o.datatype if isinstance(o, Literal) else '') for s, p, o in self.reference_graph])

    #     tp = len(test_p_o_datatypes.intersection(reference_p_o_datatypes))
    #     # unexpected 
    #     fp = len(test_p_o_datatypes) - tp
    #     # missing
    #     fn = len(reference_p_o_datatypes) - tp
    #     tn = 0

    #     precision = precision_score(tp, fp)
    #     recall = recall_score(tp, fn)
    #     f1 = f1_score(tp, fp, fn)

    #     return {'test_p_o_datatypes': list(test_p_o_datatypes), 'reference_p_o_datatypes': list(reference_p_o_datatypes), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    def objects(self) -> dict: 
        test_o = list([str(o) for s, p, o in self.test_graph])
        reference_o = list([str(o) for s, p, o in self.reference_graph])

        tp = len(overlapping_lists(test_o,reference_o))
        fp = len(test_o) - tp
        fn = len(reference_o) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_o': list(test_o), 'reference_o': list(reference_o), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    def objects_uris(self) -> dict: 
        test_o = list([str(o) for s, p, o in self.test_graph if isinstance(o, URIRef)])
        reference_o = list([str(o) for s, p, o in self.reference_graph if isinstance(o, URIRef)])

        tp = len(overlapping_lists(test_o,reference_o))
        fp = len(test_o) - tp
        fn = len(reference_o) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_o': list(test_o), 'reference_o': list(reference_o), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    # without datatype is the relaxed version
    def objects_literals(self) -> dict: 
        test_o = list([str(o) for s, p, o in self.test_graph if isinstance(o, Literal)])
        reference_o = list([str(o) for s, p, o in self.reference_graph if isinstance(o, Literal)])

        tp = len(overlapping_lists(test_o,reference_o))
        fp = len(test_o) - tp
        fn = len(reference_o) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_o': list(test_o), 'reference_o': list(reference_o), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    @todo("implement with sparl query")
    def predicate_datatypes(self):
        test_p_o = list([str(p)+str(o.datatype) for s, p, o in self.test_graph if isinstance(o, Literal)])
        reference_p_o = list([str(p)+str(o.datatype) for s, p, o in self.reference_graph if isinstance(o, Literal)])

        tp = len(overlapping_lists(test_p_o,reference_p_o))
        fp = len(test_p_o) - tp
        fn = len(reference_p_o) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_p_o': list(test_p_o), 'reference_p_o': list(reference_p_o), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    @todo("implement with sparl query")
    def predicate_datatypes_unique(self):
        test_p_o = set([str(p)+str(o.datatype) for s, p, o in self.test_graph if isinstance(o, Literal)])
        reference_p_o = set([str(p)+str(o.datatype) for s, p, o in self.reference_graph if isinstance(o, Literal)])

        tp = len(test_p_o.intersection(reference_p_o))
        fp = len(test_p_o) - tp
        fn = len(reference_p_o) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)

        return {'test_p_o': list(test_p_o), 'reference_p_o': list(reference_p_o), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}

    def subjects_classes():
        pass

    def subjects_classes_fuzzy():
        pass

    def predicate_range(self):
        pass

    def predicate_range_unique(self):
        pass

    def specific_predicate_scores(self):
        pass

    dbo = "http://dbpedia.org/ontology/"
    LIST_OF_SUFFIX = [
        "title",
        "orinalTitle",
        "starring",
        "editor",
        "producer",
        "editing",
        "director",
        "composer",
        "runtime",
        "Work/runtime",
        "birthYear",
        "deathYear",
        "genre",
        "name",
        "startYear",
    ]

    LIST_OF_PREDICATES = [
        dbo+"starring",
        dbo+"editor",
        dbo+"producer",
        dbo+"editing",
        dbo+"director",
        dbo+"composer",
        dbo+"runtime",
        dbo+"Work/runtime",
        dbo+"birthYear",
        dbo+"genre",
        dbo+"name",
        dbo+"title",
        dbo+"startYear",
    ]

    def predicateMatch(self):
        """check if a predicate is used in the test graph 
        between equivalent subject object pairs of the reference graph"""
        # subjectAlignment
        result = {}
        for target_property in self.LIST_OF_PREDICATES:

            result[target_property] = self.checkProperty(target_property)
        return result
    

    def inversePredicateMatch(self):
        """
        check if a predicate is used in the inverse direction in the test graph
        between equivalent subject object pairs of the reference graph
        """
        # subjectAlignment
        pass

    
    def countPersonIds(self):
        personIds = set(idsByType['http://dbpedia.org/ontology/Person'])
        print(len(personIds))
        s_list = set([ str(s) for s, p, o in self.test_graph if str(s).startswith('http://mykg.org/resource/')])

        count = 0
        for s in s_list:
            if any(id in s for id in personIds):
                count += 1

        return count

    def allPersonHaveId(self):
        personIds = set(idsByType['http://dbpedia.org/ontology/Person'])
        s_list = set([ str(s) for s, p, o in self.test_graph if str(s).startswith('http://mykg.org/resource/')])

        count = 0

        for personId in personIds:
            if any(personId in s for s in s_list):
                count += 1

        return 1 if len(personIds) == count else 0
    
    def allAHaveId(self):
        actorIds = set(idsByType['http://dbpedia.org/ontology/Actor'])
        s_list = set([ str(s) for s, p, o in self.test_graph if str(s).startswith('http://mykg.org/resource/')])

        count = 0

        for actorId in actorIds:
            if any(actorId in s for s in s_list):
                count += 1

        return 1 if len(actorIds) == count else 0

    def countActorIds(self):
        actorIds = set(idsByType['http://dbpedia.org/ontology/Actor'])
        s_list = set([ str(s) for s, p, o in self.test_graph if str(s).startswith('http://mykg.org/resource/')])

        count = 0
        for s in s_list:
            if any(id in s for id in actorIds):
                count += 1

        return count
    
    def countPersonIdsPersonType(self):
        personIds = set(idsByType['http://dbpedia.org/ontology/Person'])
        s_list = set([str(s) for s, p, o in self.test_graph if str(s).startswith('http://mykg.org/resource/') and str(p) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and str(o) == 'http://dbpedia.org/ontology/Person'])

        count = 0
        for s in s_list:
            if any(id in s for id in personIds):
                count += 1

        return count

    def countActorIdsActorType(self):
        personIds = set(idsByType['http://dbpedia.org/ontology/Actor'])
        s_list = set([ str(s) for s, p, o in self.test_graph if str(s).startswith('http://mykg.org/resource/') and str(p) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and str(o) == 'http://dbpedia.org/ontology/Actor'])

        count = 0
        for s in s_list:
            if any(id in s for id in personIds):
                count += 1

        return count

    def allTargetPredicatesMapped(self):
        p_test_set = set([ str(p) for s, p, o in self.test_graph])
        p_reference_set = set([ str(p) for s, p, o in self.reference_graph])

        overlap = p_test_set.intersection(p_reference_set)

        return 1 if len(overlap) == len(p_reference_set) else 0

    def onlyTargetPredicatesMapped(self):
        p_test_set = set([ str(p) for s, p, o in self.test_graph])
        p_reference_set = set([ str(p) for s, p, o in self.reference_graph])

        overlap = p_test_set.intersection(p_reference_set)

        return 1 if len(overlap) == len(p_test_set) else 0

    def countPredicate(self, predicate):
        return len([ str(s) for s, p, o in self.test_graph if str(p) == predicate])

    def countPredicateLiteral(self, predicate):
        return len([ str(s) for s, p, o in self.test_graph if str(p) == predicate and isinstance(o, Literal)])
    
    def countPredicateObject(self, predicate):
        return len([ str(s) for s, p, o in self.test_graph if str(p) == predicate and not isinstance(o, Literal)])

    def magnifiedPredicatesStats(self) -> dict:
        p_list = set([ str(p) for s, p, o in self.reference_graph]+["http://dbpedia.org/ontology/editor", "http://dbpedia.org/ontology/runtime", "http://dbpedia.org/ontology/producer"]) 
        
        hbs = HiearchyBasedScores(graph_onto, self.reference_graph, self.test_graph)
        results = {}
        for predicate in p_list:
            
            #p used
            #p outdegr. OK
            #p used as ObjectProp.
            #p used as DtProp.
            #val+dt OK
            #o fuzzy OK 

            directScore = hbs.propertyScoreDirect(predicate)
            # results[predicate] = {
            #     'p_used_expected': directScore['tp'] + directScore['fn'],
            #     'p_used': self.countPredicate(predicate),
            #     'o_fuzzy_OK': directScore['tp'],
            #     'p_used_as_ObjectProp': self.countPredicateObject(predicate),
            #     'p_used_as_DtProp': self.countPredicateLiteral(predicate),
            #     'val_dt_OK': hbs.propertyScoreDirectDatatype(predicate)['tp']
            # }
            expected = directScore['tp'] + directScore['fn']
            results[predicate] = {
                'p_used': 1 if self.countPredicate(predicate) > 0 else 0,
                'p outdegr_OK': 1 if self.countPredicate(predicate) == expected else 0,
                'o_fuzzy_OK': 1 if directScore['tp'] == expected else 0,
                'p_used_as_ObjectProp': 1 if self.countPredicateObject(predicate) > 0 else 0,
                'p_used_as_DtProp': 1 if self.countPredicateLiteral(predicate) > 0 else 0,
                'val_dt_OK': 1 if hbs.propertyScoreDirectDatatype(predicate)['tp'] == expected else 0
            }

        return results

    def additionalStats(self) -> dict:

        return {
            'countPersonIds': self.countPersonIds(),
            'countActorIds': self.countActorIds(),
            'countPersonIdsPersonType': self.countPersonIdsPersonType(),
            'countActorIdsActorType': self.countActorIdsActorType(),
            'allPersonHaveId': self.allPersonHaveId(),
            'allAHaveId': self.allAHaveId(),
            'allTargetPredicatesMapped': self.allTargetPredicatesMapped(),
            'onlyTargetPredicatesMapped': self.onlyTargetPredicatesMapped()
        }

    def createStatistics(self) -> dict:

        with open("kg_tests/resources/llm4rml/rml-ontology_parsed.ttl", "r") as f:
            ONTOLOGY_DATA = f.read()

        graph_onto = Graph().parse(data=ONTOLOGY_DATA, format="turtle")

        dbo = "http://dbpedia.org/ontology/"
        properties_to_check = [dbo+"starring", dbo+"editor", dbo+"producer", dbo+"editing", dbo+"director", dbo+"composer", dbo+"runtime", dbo+"birthYear", dbo+"genre", dbo+"name", dbo+"title", dbo+"startYear"]


        # TODO mappings 
        # TODO respect hiearachy for classes and predicates
        # TODO check gold standard
        # TODO rename metrics predicate_* > predicate_range_*
        # TODO plots: only build the average with the valid RDF triples
        return {
            'triples': self.tripleScore(),
            'subjects': self.subjects(),
            'subjects_fuzzy': self.subjects_fuzzy(),
            'predicates': self.properties(),
            'predicates_unique': self.properties_unique(),
            'classes': self.classes(),
            'classes_unique': self.classes_unique(),
            'objects': self.objects(),
            'objects_uris': self.objects_uris(),
            'objects_literals': self.objects_literals(),
            'predicate_datatype_range' : self.predicate_datatypes(),
            'predicate_datatype_range_unique': self.predicate_datatypes_unique(),
            # 'subjects_classes': self.subjects_classes(),
            # 'subjects_classes_fuzzy': self.subjects_classes_fuzzy(),
            'classes_transitive': HiearchyBasedScores(graph_onto, self.reference_graph, self.test_graph).class_sim_scores(),
            'predicates_transitive': HiearchyBasedScores(graph_onto, self.reference_graph, self.test_graph).property_sim_scores(),
            'single_property_scores': HiearchyBasedScores(graph_onto, self.reference_graph, self.test_graph).checkProperties(properties_to_check),
            'predicates_direct' : HiearchyBasedScores(graph_onto, self.reference_graph, self.test_graph).propertiesScoresDirect(),
            'predicates_inverse' : HiearchyBasedScores(graph_onto, self.reference_graph, self.test_graph).propertiesScoresInverse(),
            # 'specific_predicate_scores': self.specific_predicate_scores()
    }


class RDFSparqlMetrics():

    def __init__(self, graph) -> None:
        self.graph = graph

    def entityByPAndO(self, p, o):
        results = self.graph.query(f"""
                    SELECT ?s
                    WHERE {{
                        ?s {p} {o} .
                    }}
                    """)
        for result in results:
            yield str(result[0])

def fuzzyGraphMatch(test_graph: Graph, reference_graph: Graph):
    pass


# l1 = ["hallo", "welt", "und", "welt", "und", "andere"]
# l2 = ["hallo", "du", "und", "hallo", "er", "und", "hallo", "welt"]

# print(overlapping_lists(l1, l2))

# graph = Graph()
# graph.parse(data=open('/workspace/papers/llm4rml/kg-pipeline/target/output/gold.ttl', 'r').read(), format='turtle')

# sm = RDFSparqlMetrics(graph)

# tmp = sm.entityByPAndO("<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "<http://dbpedia.org/ontology/Film>")

# print(list(tmp))

# tmp2 = sm.entityByPAndO("<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "<http://dbpedia.org/ontology/Film>")

# q = prepareQuery(
#     "SELECT ?s WHERE { ?person foaf:knows ?s .}",
#     initNs = { "foaf": FOAF }
# )

# g = rdflib.Graph()
# g.parse("foaf.rdf")

# tim = rdflib.URIRef("http://www.w3.org/People/Berners-Lee/card#i")

# for row in g.query(q, initBindings={'person': tim}):
#     print(row)