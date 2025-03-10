package ai.scads.kg.core

import org.apache.jena.query.{QueryExecutionFactory, QueryFactory, ReadWrite}
import org.apache.jena.riot.{Lang, RDFDataMgr}
import org.apache.jena.system.Txn
import org.apache.jena.tdb2.TDB2Factory

object MetaKG extends App {

  def update(): Unit = {

  }

  val ds = TDB2Factory.connectDataset("target/tdb2")

  Txn.executeWrite(ds, () => {
    RDFDataMgr.read(ds,"example.ttl")
    println("RDF data loaded into TDB2 store")
  })

  val QUERY =
    """SELECT * {
      |  ?s ?p ?o .
      |}
      |""".stripMargin


  Txn.executeRead(ds, () => {
    val res = QueryExecutionFactory.create(QueryFactory.create(QUERY),ds).execSelect()
    while (res.hasNext) {
      val qs = res.next()
      println(qs.get("?s"),qs.get("?p"),qs.get("?o"))
    }
  })


//  Txn.execWrite(ds, () => {
//    RDFDataMgr.read(ds, "SomeData.ttl")
//
//  })

//  Txn.execRead(dsg, () => {
//    RDFDataMgr.write(System.out, ds, Lang.TRIG)
//  })

  object MetaKGBindAnnotation {


  }

  object Vocab {

    val BASE = "https://vehnem.github.com/kgflex/"


  }
}
