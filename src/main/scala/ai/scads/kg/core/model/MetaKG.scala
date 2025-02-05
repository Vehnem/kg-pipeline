package ai.scads.kg.core.model

import ai.scads.kg.core.graph.RDFGraph
import org.apache.jena.rdf.model.{ModelFactory, ResourceFactory, Statement}

import scala.jdk.CollectionConverters._
import scala.reflect.io.File

/**
 * Class to build the meta kg
 */
class MetaKG extends RDFGraph {

  override val graphName: String = ""

  override def listStatements: List[(String, String, String)] = List()

  private val model = ModelFactory.createDefaultModel()

  object ImplicitFunctions {
    implicit class StatementTuple(tuple3: (String, String, String)) {
      def stmt: Statement = {
        ResourceFactory.createStatement(
          ResourceFactory.createResource(s"http://base.org/${tuple3._1}"),
          ResourceFactory.createProperty(s"http://base.org/${tuple3._2}"),
          ResourceFactory.createResource(s"http://base.org/${tuple3._3}")
        )
      }
    }
  }

  def add(entity: MetaEntity): Unit = {
    // call function here
    import ImplicitFunctions._

    entity.toStatement.map(_.stmt).foreach({
      st =>
        println(st.toString)
        model.add(st)
    })
  }

  def query(queryString: String): Unit = {

  }

  def show(): Unit = {
    model.listStatements().asScala.foreach(println)
  }
}

case class Tool(id: String,
                @statement name: String
               ) extends MetaEntity

object MetaKG extends App {

//  val mkg = new MetaKG()
//
//  mkg.add(Tool("toolA", "someName"))
//
//  mkg.show()
//
//  def create(conf: MetaKGConf): MetaKG = {
//    new MetaKG
//  }
}

class MetaKGBuilder extends App {

  // TODO read the google spreadsheet
  def readDefinition(file: File): Unit = {

  }

  def writeDefintion(): Unit = {

  }
}
