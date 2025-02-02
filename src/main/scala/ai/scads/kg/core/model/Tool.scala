package ai.scads.kg.core.model


/**
 * A tool defintiion for the KG Pipleine Meta Graph
 * A tool is used to execute a specific process that is required for knowledge graph integration
 * Like: Extraction, Matching, Mapping, Fusion, Completion
 */
trait Tool {

  private type ConfigType = String

  val config: ConfigType
  val io: IOType

  // TODO can be hierarchically
  type Category = String
  val category: Category

}

trait IOType {

  type FlowType = String

  val flow: FlowType
  val input: List[Data]
  val output: List[Data]

}

trait Data {

  /**
   * Batch or Stream
   */
  type FlowType = String

  val format: DataFormat
  val flowType: FlowType
}

/**
 * A serialized format
 * Json, XML, HTML
 * NTriples, Turtle, NQuads
 */
//trait DataFormat {
//
//  /**
//   * A grouping data class
//   * like "NESTED" for XML, JSON, YAML
//   * or like "RDF" for NTriples, NQuads
//   * or like "Tabular" for CSV, TSV, SQL
//   */
//  type ClassType = String
//  type MimeType = String
//
//  val `classes` : List[ClassType]
//  val mimeType: MimeType
//}


