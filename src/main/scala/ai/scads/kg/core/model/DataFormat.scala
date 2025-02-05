package ai.scads.kg.core.model

///**
// * TODO format vs structure vs intention?
// */
sealed trait DataFormat { def name: String }
case object NTripleFormat extends DataFormat { val name = "application/n-triples" }
case object XMLFormat extends DataFormat { val name = "text/xml" }
case object JsonFormat extends DataFormat { val name = "application/json" }
case object CSVFormat extends DataFormat { val name = "text/csv" }
