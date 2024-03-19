from rdflib import Graph
from rdflib.term import URIRef, Literal
import json
from collections import defaultdict




SUBCLASSOF_QUERY="""
SELECT ?superClass ?subClass
WHERE {
    ?subClass rdfs:subClassOf ?superClass .
}
"""

SUBPROPERTYOF_QUERY="""
SELECT ?superProperty ?subProperty
WHERE {
    ?subProperty rdfs:subPropertyOf ?superProperty .
}
"""

SUBJECT_CLASS_QUERY="""
SELECT ?class
WHERE {
    ?s a ?class .
}
"""

SUBJECT_PROPERTY_QUERY="""
SELECT ?property
WHERE {
    ?s ?property ?o .
}
"""

SUBJECT_PROPERTY_VALUE_QUERY="""
SELECT ?property ?value
WHERE {
    ?s ?property ?value .
}"""

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
    "Work/runtime"
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

def precision_score(tp, fp):
    return tp / (tp + fp) if tp + fp > 0 else 0

def recall_score(tp, fn):
    return tp / (tp + fn) if tp + fn > 0 else 0

def f1_score(tp, fp, fn):
    precision = precision_score(tp, fp)
    recall = recall_score(tp, fn)
    return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0


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

class HiearchyBasedScores:
    """Only valid when reference is the most specific"""

    def __init__(self, ontology_graph, reference_graph, test_graph):
        self.ontology_graph = ontology_graph
        self.reference_graph = reference_graph
        self.test_graph = test_graph
        self.class_paths = self.transitive_closure(self.class_relations(ontology_graph))
        self.property_paths = self.transitive_closure(self.property_relations(ontology_graph))
        self.subject_alignment = self.subject_alignment(test_graph, reference_graph, "http://mykg.org/resource/")

    
    @staticmethod
    def class_relations(ontology_graph):
        classes = set()
        class_relations = {}
        subclassof_query_result = ontology_graph.query(SUBCLASSOF_QUERY)
        for result in subclassof_query_result:
            super_class = str(result[0])
            sub_class = str(result[1])
            classes.add(sub_class)
            classes.add(super_class)
            class_relations[sub_class] = super_class
        return class_relations

    @staticmethod
    def property_relations(ontology_graph):
        properties = set()
        property_relations = {}
        subpropertyof_query_result = ontology_graph.query(SUBPROPERTYOF_QUERY)
        for result in subpropertyof_query_result:
            super_property = str(result[0])
            sub_property = str(result[1])
            properties.add(sub_property)
            properties.add(super_property)
            property_relations[sub_property] = super_property
        return property_relations


    @staticmethod
    def transitive_closure(subClassDict):
        classes = set(subClassDict.keys()) | set(subClassDict.values())
        closure = defaultdict(list)
        for sub_class_name in classes:
            class_name = sub_class_name
            closure[sub_class_name].append(class_name)
            # print("outer", class_name)
            while subClassDict.get(class_name):
                class_name = subClassDict[class_name]
                closure[sub_class_name].append(class_name)
                # print("inner", class_name)
        return closure

    @staticmethod
    def hierachy_sim_score(reference_resource, test_resource, hiearachy_paths):
        if reference_resource == test_resource:
            return 1
        elif test_resource in hiearachy_paths[reference_resource]:
            path = hiearachy_paths[reference_resource]
            distance = path.index(test_resource)
            return 0.5 ** distance
        elif reference_resource in hiearachy_paths[test_resource]:
            return 0 # TODO
        else:
            return 0

    
    @staticmethod
    def subject_alignment(test_graph, reference_graph, reference_prefix) -> list:
        test_graph_subjecIRIs = set([s for s, p, o in test_graph])
        reference_graph_subjectIRIs = set([s for s, p, o in reference_graph])
        reference_ids = [str(s).split("/")[-1] for s in reference_graph_subjectIRIs]
        res = []
        for s in test_graph_subjecIRIs:
            # matched = False
            for id in reference_ids:
                if id in str(s) and str(s).startswith(reference_prefix):
                    res.append((reference_prefix+id,str(s)))
        return res

    def property_alignment(self, s_alignments) -> list:
        sRefBysTest = {}
        for s_align in s_alignments:
            sRefBysTest[s_align[1]] = s_align[0]

        reference_so_p_list = [(  str(s)+str(o)  ,   str(p)) for s, p, o in self.reference_graph]
        test_so_p_list = [(   sRefBysTest.get(str(s),str(s))+sRefBysTest.get(str(o)   ,   str(o)),str(p)) for s, p, o in self.test_graph]
        
        # print(json.dumps(reference_so_p_list, indent=2))
        # print(json.dumps(test_so_p_list, indent=2))

        p_pairs = set()
        # get p_pairs for matches of so in reference_so_p and test_so_p
        for ref_so_p in reference_so_p_list:
            for test_so_p in test_so_p_list:
                if ref_so_p[0] == test_so_p[0]:
                    p_pairs.add((ref_so_p[1],test_so_p[1]))

        # (ref_p, test_p)
        return list(p_pairs)
    
    def subject_property_alignment(self, s_alignments) -> list:
        sRefBysTest = {}
        for s_align in s_alignments:
            sRefBysTest[s_align[1]] = s_align[0]

        reference_so_p_list = [(  str(s)+str(o)  ,   str(p)) for s, p, o in self.reference_graph]
        test_so_p_list = [(   sRefBysTest.get(str(s),str(s))+sRefBysTest.get(str(o)   ,   str(o)),str(p)) for s, p, o in self.test_graph]
        
        # print(json.dumps(reference_so_p_list, indent=2))
        # print(json.dumps(test_so_p_list, indent=2))

        p_pairs = list()
        # get p_pairs for matches of so in reference_so_p and test_so_p
        for ref_so_p in reference_so_p_list:
            for test_so_p in test_so_p_list:
                if ref_so_p[0] == test_so_p[0]:
                    p_pairs.append((ref_so_p[1],test_so_p[1]))

        # (ref_p, test_p)
        return p_pairs

    @staticmethod
    def get_specifc_class(subject, graph):
        resultSet = graph.query(SUBJECT_CLASS_QUERY.replace("?s","<"+subject+">"))
        for result in resultSet:
            return str(result[0])

    # class_paths = transitive_closure(class_relations)
    # property_paths = transitive_closure(property_relations)

    def class_sim_score(self, reference_resource, test_resource):
        return HiearchyBasedScores.hierachy_sim_score(reference_resource, test_resource, self.class_paths)

    def property_sim_score(self, reference_resource, test_resource):
        return HiearchyBasedScores.hierachy_sim_score(reference_resource, test_resource, self.property_paths)
    
    @staticmethod
    def average(scores):
        if len(scores) > 0:
            return sum(scores) / len(scores)
        else:
            return 0

    def class_sim_scores(self):
        scores = []
        s_alings = self.subject_alignment

        s_ref = list(set([ str(s) for s, p, o in self.reference_graph]))
        s_test = list(set([ str(s) for s, p, o in self.test_graph]))

        for s_aling in s_alings:
            ref_class = self.get_specifc_class(s_aling[0], self.reference_graph)
            test_class = self.get_specifc_class(s_aling[1], self.test_graph)
            scores.append((ref_class, test_class, self.class_sim_score(ref_class, test_class )))

        precission = self.average([score[2] for score in scores])
        # TODO check recall calculation
        recall = len([score[2] for score in scores if score[2] > 0])/len(s_ref)
        f1 = (2*precission*recall)/(precission+recall) if (precission+recall) > 0 else 0

        return {'f1': f1, 'precision': precission, 'recall': recall, 'precision_scores': scores, 's_ref': s_ref, 's_test': s_test}
    
    def property_sim_scores(self):
        scores = []
        s_alings = self.subject_alignment
        p_aligns = self.property_alignment(s_alings)

        p_ref = list(set([ str(p) for s, p, o in self.reference_graph]))
        p_test = list(set([ str(p) for s, p, o in self.test_graph]))

        for p_align in p_aligns:
            ref_property = p_align[0]
            test_property = p_align[1]
            scores.append((ref_property, test_property, self.property_sim_score(ref_property, test_property )))

        precssion = self.average([score[2] for score in scores])
        recall = len([score[2] for score in scores if score[2] > 0])/len(p_ref)
        f1 = (2*precssion*recall)/(precssion+recall) if (precssion+recall) > 0 else 0

        return {'f1': f1, 'precision': precssion, 'recall': recall, 's_alings': s_alings, 'p_aligns': p_aligns, 'precision_scores': scores, 'p_ref': p_ref, 'p_test': p_test}


    def propertyScoreDirect(self, target_property):
        scores = []

        sRefBysTest = {}
        for s_align in self.subject_alignment:
            sRefBysTest[s_align[1]] = s_align[0]

        ref_spo_list = [(str(s)+str(p)+str(o)) for s, p, o in self.reference_graph if str(p) == target_property]
        test_spo_list = [(sRefBysTest.get(str(s),str(s))+str(p)+sRefBysTest.get(str(o),str(o))) for s, p, o in self.test_graph if str(p) == target_property]
        
        tp = len(overlapping_lists(test_spo_list,ref_spo_list))
        fp = len(test_spo_list) - tp
        fn = len(ref_spo_list) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)
        
        return {'precision': precision, 'recall': recall, 'f1': f1, 'tp': tp, 'fp': fp, 'fn': fn}

    def propertyScoreDirectDatatype(self, target_property):
        scores = []

        sRefBysTest = {}
        for s_align in self.subject_alignment:
            sRefBysTest[s_align[1]] = s_align[0]

        ref_spo_list = [(str(s)+str(p)+str(o)+str(o.datatype)) for s, p, o in self.reference_graph if str(p) == target_property and isinstance(o, Literal)]
        test_spo_list = [(sRefBysTest.get(str(s),str(s))+str(p)+str(o)+str(o.datatype)) for s, p, o in self.test_graph if str(p) == target_property and isinstance(o, Literal)]
        
        tp = len(overlapping_lists(test_spo_list,ref_spo_list))
        fp = len(test_spo_list) - tp
        fn = len(ref_spo_list) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)
        
        return {'precision': precision, 'recall': recall, 'f1': f1, 'tp': tp, 'fp': fp, 'fn': fn}

    def propertyScoreInverse(self, target_property):
        scores = []

        sRefBysTest = {}
        for s_align in self.subject_alignment:
            sRefBysTest[s_align[1]] = s_align[0]

        ref_spo_list = [(str(s)+str(p)+str(o)) for s, p, o in self.reference_graph if str(p) == target_property]
        test_ops_list = [(sRefBysTest.get(str(o),str(o))+str(p)+sRefBysTest.get(str(s),str(s))) for s, p, o in self.test_graph if str(p) == target_property]
        
        tp = len(overlapping_lists(test_ops_list,ref_spo_list))
        fp = len(test_ops_list) - tp
        fn = len(ref_spo_list) - tp
        tn = 0

        precision = precision_score(tp, fp)
        recall = recall_score(tp, fn)
        f1 = f1_score(tp, fp, fn)
        
        return {'precision': precision, 'recall': recall, 'f1': f1}


    def propertiesScoresDirect(self):
        result = {}
        for target_property in LIST_OF_PREDICATES:
            result[target_property] = self.propertyScoreDirect(target_property)
        return result
        
    def propertiesScoresInverse(self):
        result = {}
        for target_property in LIST_OF_PREDICATES:
            result[target_property] = self.propertyScoreInverse(target_property)
        return result

##############
# NEW METRICS
##############
    
# problem
# precision is only calculated for a single property alignment

    def checkProperty(self, target_property):
        scores = []
        s_alings = self.subject_alignment
        p_aligns = self.subject_property_alignment(s_alings)
        p_aligns = [p_aling for p_aling in p_aligns if p_aling[0] == target_property]

        p_ref = [str(p) for s, p, o in self.reference_graph if str(p) == target_property]

        for p_align in p_aligns:
            ref_property = p_align[0]
            test_property = p_align[1]
            scores.append((ref_property, test_property, self.property_sim_score(ref_property, test_property )))

        precssion = self.average([score[2] for score in scores])
        recall = len([score[2] for score in scores if score[2] > 0])/len(p_ref) if len(p_ref) > 0 else 0 #TODO
        f1 = (2*precssion*recall)/(precssion+recall) if (precssion+recall) > 0 else 0

        return {'f1': f1, 'precision': precssion, 'recall': recall } #'s_alings': s_alings, 'p_aligns': p_aligns, 'precision_scores': scores, 'p_ref': p_ref, 'p_test': "TODO filter"}

    def checkProperties(self, target_properties):
        result = {}
        for target_property in target_properties:
            result[target_property] = self.checkProperty(target_property)
        return result


