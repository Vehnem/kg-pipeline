package ai.scads.kg.core.graph

import org.apache.jena.rdf.model.ModelFactory
import scala.jdk.CollectionConverters._

class JenaRdfGraph(override val graphName: String) extends RDFGraph {

  private val model = ModelFactory.createDefaultModel()

  override def listStatements: List[(String, String, String)] =
    model.listStatements().toList.asScala.map(stmt => (stmt.getSubject.toString,stmt.getPredicate.toString,stmt.getObject.toString)).toList
}
