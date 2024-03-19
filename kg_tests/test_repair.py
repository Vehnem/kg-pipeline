from rdflib import Graph

DATA='''
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix rml: <http://semweb.mmlab.be/ns/rml#> .
@prefix ql: <http://semweb.mmlab.be/ns/ql#> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix : <http://example.org/rules#> .

:FilmMap a rr:TriplesMap;
    rml:logicalSource [
        rml:source "USER_INPUT";
        rml:referenceFormulation ql:JSONPath;
        rml:iterator "$"
    ];
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Film
    ];
    rr:predicateObjectMap [
        rr:predicate dbo:endYear;
        rr:objectMap [ rml:reference "endYear" ]
    ],
    rr:predicateObjectMap [
        rr:predicate dbo:startYear;
        rr:objectMap [ rml:reference "startYear" ]
    ],
    rr:predicateObjectMap [
        rr:predicate dbo:originalTitle;
        rr:objectMap [ rml:reference "originalTitle" ]
    ],
    rr:predicateObjectMap [
        rr:predicate dbo:title;
        rr:objectMap [ rml:reference "primaryTitle" ]
    ];

:PersonMap a rr:TriplesMap;
    rml:logicalSource [
        rml:source "USER_INPUT";
        rml:referenceFormulation ql:JSONPath;
        rml:iterator "$.involvedPeople[*]"
    ];
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Person
    ];
    rr:predicateObjectMap [
        rr:predicate dbo:birthYear;
        rr:objectMap [ rml:reference "birthYear" ]
    ];

:ActorMap a rr:TriplesMap;
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Actor; rr:condition [
            rml:reference "category";
            rr:referenceFormulation ql:JSONPath; 
            rr:equals "actor"
        ]
    ];

:DirectorMap a rr:TriplesMap;
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Director; rr:condition [
            rml:reference "category";
            rr:referenceFormulation ql:JSONPath;
            rr:equals "director"
        ]
    ];

:ProducerMap a rr:TriplesMap;
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Producer; rr:condition [
            rml:reference "category";
            rr:referenceFormulation ql:JSONPath;
            rr:equals "producer"
        ]
    ];

:ComposerMap a rr:TriplesMap;
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Composer; rr:condition [
            rml:reference "category";
            rr:referenceFormulation ql:JSONPath;
            rr:equals "composer"
        ]
    ];

:EditorMap a rr:TriplesMap;
    rr:subjectMap [
        rr:template "http://dbpedia.org/resource/{id}";
        rr:class dbo:Editor; rr:condition [
            rml:reference "category";
            rr:referenceFormulation ql:JSONPath;
            rr:equals "editor"
        ]
    ];
'''
    
def test_turtle_repair():
    g = Graph()

    try:
        g.parse(format='turtle', data=DATA)
    except Exception as e:
        print(e)

    # print(g.serialize(format='turtle'))