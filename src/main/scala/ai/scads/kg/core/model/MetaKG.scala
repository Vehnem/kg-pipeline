package ai.scads.kg.core.model

import ai.scads.kg.core.graph.RDFGraph

/**
 * Class to build the meta kg
 */
class MetaKG extends RDFGraph {

  override val graphName: String = ???

  override def listStatements: List[(String, String, String)] = ???
}

object MetaKG {
  def create(conf: MetaKGConf): MetaKG = {
    new MetaKG
  }
}

