package ai.scads.kg.core.model

// 1. Data Source: Defines methods to fetch data
trait DataSource {
  def read(): Iterator[String] // Returns data as an iterator of strings (or another format)
}

// Example Implementations
class FileSource(filePath: String) extends DataSource {
  def read(): Iterator[String] = scala.io.Source.fromFile(filePath).getLines()
}

class ApiSource(apiUrl: String) extends DataSource {
  def read(): Iterator[String] = {
    // Simulate API call and return data
    Iterator("{json: data}")
  }
}
// 1. Exchange Format: Defines a common structure for processed data
case class ExchangeFormat(data: Seq[String], metadata: Map[String, String] = Map())

// 2. Data Ingestion: Fetches data from sources
trait DataIngestion {
  def ingest(source: DataSource): Seq[String] // Collects data as a sequence
}

class BatchIngestion extends DataIngestion {
  def ingest(source: DataSource): Seq[String] = source.read().toSeq
}

class StreamingIngestion extends DataIngestion {
  def ingest(source: DataSource): Seq[String] = {
    // Simulated streaming ingestion
    source.read().take(10).toSeq
  }
}

// 3. Data Processor: Transforms and cleans data
//trait DataProcessor {
//  def transform(data: Seq[String]): Seq[String] // Modify or clean data
//}
//
//class SimpleProcessor extends DataProcessor {
//  def transform(data: Seq[String]): Seq[String] = data.map(_.toUpperCase)
//}

// 4. Data Storage: Defines where processed data is stored
trait DataStorage {
  def save(data: Seq[String]): Unit
}

class DatabaseStorage extends DataStorage {
  def save(data: Seq[String]): Unit = println(s"Saving to Database: ${data.take(3)} ...")
}

class DataLakeStorage extends DataStorage {
  def save(data: Seq[String]): Unit = println(s"Saving to Data Lake: ${data.take(3)} ...")
}

// 5. Orchestration: Schedules and manages the pipeline
trait Orchestration {
  def runPipeline(): Unit
}

//class SimplePipeline(
//                      source: DataSource,
//                      ingestion: DataIngestion,
//                      processor: DataProcessor,
//                      storage: DataStorage
//                    ) extends Orchestration {
//
//  def runPipeline(): Unit = {
//    println("Starting Data Pipeline...")
//    val rawData = ingestion.ingest(source)
//    val transformedData = processor.transform(new ExchangeFormat())
//    storage.save(transformedData)
//    println("Pipeline Execution Complete!")
//  }
//}

// 6. Monitoring: Logs events and errors
trait Monitoring {
  def log(event: String): Unit
}

class ConsoleLogger extends Monitoring {
  def log(event: String): Unit = println(s"[LOG]: $event")
}

// 7. Data Consumer: Defines how data is consumed
trait DataConsumer {
  def consume(): Unit
}

class BIConsumer extends DataConsumer {
  def consume(): Unit = println("Connecting to Tableau/Power BI for reporting.")
}

class MLModelConsumer extends DataConsumer {
  def consume(): Unit = println("Fetching data for ML model training.")
}

// 4. Data Pipeline with Processing Chain
object DataPipelineApp extends App {
  // Define data source
  val rawData = ExchangeFormat(Seq("hello", "", "world", "scala", "", "pipeline"))

  // Create processors
  val uppercaseProcessor = new UppercaseProcessor
  val filterProcessor = new FilterEmptyProcessor
  val timestampProcessor = new TimestampProcessor

  // Chain processors together
  uppercaseProcessor.setNext(filterProcessor).setNext(timestampProcessor)

  // Execute pipeline
  val processedData = uppercaseProcessor.process(rawData)

  // Output result
  println(s"Processed Data: ${processedData.data}")
  println(s"Metadata: ${processedData.metadata}")
}


// 2. Abstract Data Processor: Supports Chaining
trait DataProcessor {
  var nextProcessor: Option[DataProcessor] = None

  // Process the data and pass to the next processor if available
  def process(input: ExchangeFormat): ExchangeFormat = {
    val transformedData = transform(input)
    nextProcessor match {
      case Some(next) => next.process(transformedData) // Pass to next processor
      case None       => transformedData // End of chain
    }
  }

  // Abstract method to implement processing logic
  def transform(input: ExchangeFormat): ExchangeFormat

  // Allows setting the next processor dynamically
  def setNext(processor: DataProcessor): DataProcessor = {
    nextProcessor = Some(processor)
    processor // Return the processor to allow chaining
  }
}

// 3. Example Data Processors

// Converts text to uppercase
class UppercaseProcessor extends DataProcessor {
  def transform(input: ExchangeFormat): ExchangeFormat = {
    val updatedData = input.data.map(_.toUpperCase)
    input.copy(data = updatedData, metadata = input.metadata + ("Uppercase" -> "Applied"))
  }
}

// Filters out empty strings
class FilterEmptyProcessor extends DataProcessor {
  def transform(input: ExchangeFormat): ExchangeFormat = {
    val updatedData = input.data.filter(_.nonEmpty)
    input.copy(data = updatedData, metadata = input.metadata + ("FilterEmpty" -> "Applied"))
  }
}

// Appends a timestamp to the metadata
class TimestampProcessor extends DataProcessor {
  def transform(input: ExchangeFormat): ExchangeFormat = {
    val updatedMetadata = input.metadata + ("Timestamp" -> System.currentTimeMillis().toString)
    input.copy(metadata = updatedMetadata)
  }
}


