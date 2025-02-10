package ai.scads.kg.core.model

sealed trait DataFormat { def name: String }
class AnyFormat extends DataFormat { val name = "*/*" }
class NTripleFormat extends DataFormat { val name = "application/n-triples" }
case object XMLFormat extends DataFormat { val name = "text/xml" }
case object JsonFormat extends DataFormat { val name = "application/json" }
case object CSVFormat extends DataFormat { val name = "text/csv" }

class EmbeddedDataFormat[OUTER <: DataFormat, INNER <: DataFormat]

// Line Based

sealed trait DataExchangeFormat
class EntityResolutionDEF extends DataExchangeFormat
class ExtractDEF extends DataExchangeFormat


// TODO specify difference
sealed trait DataFlow
abstract class BatchFlow[A <:DataFormat] extends DataFlow
abstract class StreamFlow[A <: DataFormat] extends DataFlow