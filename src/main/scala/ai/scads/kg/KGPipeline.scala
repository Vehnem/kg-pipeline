package ai.scads.kg

trait KGPipeline {


}

class KGPipelineImpl {


}

//import ai.scads.kg.core.model.{CSVFormat, DataFormat, JsonFormat, NTripleFormat, XMLFormat}
//
//import java.net.URI
//import scala.collection.mutable.ListBuffer
//
//
//class KGPipeline {
//
//  private val stages: ListBuffer[String] = ListBuffer[String]()
//
//  def add(stage: String): Unit = {
//    stages.append(stage)
//  }
//
//}
//
//abstract class KGSource extends Data {
//  val uri: String
//}
//
//
//abstract class SourceReader {
//
//
//}
//
//abstract class KGStageResult {
//  val generated: List[Data]
//}
//
//abstract class KGStage(kgStageResults: KGStageResult*) {
//  def run(): KGStageResult
//  // if multiple this is like a join in SPARK
//}
//
//class Stage {
//
//  def transform(f: (Seq[Data]) => Data): Unit = {
//
//  }
//}
//
//sealed trait DataClass { def name: String }
//case object RDF extends DataClass { val name = "rdf" }
//case object XML extends DataClass { val name = "xml" }
//case object JSON extends DataClass { val name = "json" }
//case object Tabular extends DataClass { val name = "tabular" }
//
//sealed trait DataFlow { def name: String }
//case object BatchFlow extends DataFlow { val name = "batch"}
//case object StreamFlow extends DataFlow { val name = "stream"}
//
//trait Data {
//
//  val location: String
//  val `class`: DataClass
//  val format: DataFormat
//  val flow: DataFlow
//
//}
//
//
//class BatchIO(data: Data) {
//
//  data.flow match {
//    case BatchFlow =>
//    case StreamFlow =>
//      throw new Exception("Data not of flow type batch")
//  }
//}
//
//class StreamIO[Data] {
//
//}
//
//class Processor[DataA,DataB] {
//
//  def run(source: DataA, target: DataB): Unit = {
//
//  }
//}
//
//trait SourceDataConnector
//
//class FileSourceConnector(source: FileSource) extends SourceDataConnector {
//
//
//
//}
//
//// Problem is that for almost every tool the input needs to prepared and the output needs to be processed
//
//// Text
//// Image
//// RDF
//// JSON
//// CSV
//// XML
//// HTML
//// Wikitext
//
//trait Source {
//
//}
//
//class FileSource(uri: URI) extends Source
//
///**
// * Idea is to build a distributed framework for kg integration
// */
//object KGPipeline extends App {
//
////  def stmt(s: String, p: String, o: String): Statement
//
//  // Extract Leipzig
//  // https://github.com/YaserJaradeh/ThePlumber
//
//  // https://www.w3.org/2001/sw/wiki/Category:Development_Environment
//
//  // https://en.wikipedia.org/wiki/Talk:Data_exchange
//
//  // Uniform Matching Output
//  // (cluster, meta)
//
//  // TODO automatic source provisioning
//
//  val format: DataFormat = NTripleFormat
//
////  calc((d1,d2) => {
////    d1*d2
////  },0)
//
//  val kgp = new KGPipeline
//
//  val sourceA = "stream of text/plain"
//  val sourceB = "batch text/turtle"
//  val sourceC = "stream of application/json"
//
//  val extractor = ""
//  val matcher = ""
//  val mapper = ""
//
//  // Target can be:
//  // 1. an ontology (new vs existing vocabulary)
//  // 2. instances (new vs existing vocabulary)
//  // 3. both
//  // 4. nothing
//  // val target = // is rdfs/owl/shacl or else
//
//  val targetOntology, targetInstances = ("","") // derv
//
//  // how updates???
//
//  // holistic
//  // sequential
//  // parallel
//  register(sourceA)
//  register(sourceB)
//  register(sourceC)
//
//  def run(): Unit = {
//    println("running for source...")
//  }
//
//  def register(any: Any): Unit = {
//
//  }
//
//
//  def write(): Unit = {
//
//  }
//
//}
