package ai.scads.kg.core.model

/**
 * TODO format vs structure vs intention?
 */
trait DataClass

trait DataFormat {

  val `class`: DataClass
}


class RDF extends DataFormat
