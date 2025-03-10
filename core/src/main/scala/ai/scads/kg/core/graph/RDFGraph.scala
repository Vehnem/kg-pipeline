package ai.scads.kg.core.graph

abstract class RDFGraph extends DirectGraph {

  val graphName: String

  def listStatements: List[(String,String,String)]
}