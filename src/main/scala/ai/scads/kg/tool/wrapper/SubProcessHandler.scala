package ai.scads.kg.tool.wrapper

import com.typesafe.config.ConfigFactory
import org.apache.commons.io.IOUtils
import org.slf4j.LoggerFactory

import java.io.File
import scala.io.Source

//import ai.scads.kg.core.model.IOType

/**
 * A FaultTolerant SubProcessHandler
 * What is needed:
 * - ExecutionMode
 */
class SubProcessHandler(config: String/*ProcessConfig*/) {

  type ExecutionMode = String

  val executionMode: ExecutionMode = null
//  val IO: IOType = null


  def run(): Unit = {

    executionMode match {
      case "CLI" =>
//        IO.flow match {
//          case "BATCH" =>
//        }
      case "API" =>

      case "HTTP" =>

    }

  }
}

import com.typesafe.config.{Config, ConfigFactory}
import scala.jdk.CollectionConverters._

case class DataFlow(flow: String, format: String)
case class Data(consumes: DataFlow, produces: DataFlow)
case class ToolConfig(name: String, `type`: String, category: String, entry: String, data: Data)

object ConfigParser {
  def loadConfig(): ToolConfig = {
    val config: Config = ConfigFactory.parseFile(new File("/home/marvin/paper/kgpipeline/kg-pipeline/src/test/resources/example-def.conf")) // Assumes your file is tool.conf in src/main/resources

    ToolConfig(
      name = config.getString("name"),
      `type` = config.getString("type"),
      category = config.getString("category"),
      entry = config.getString("entry"),
      data = Data(
        consumes = DataFlow(
          flow = config.getString("data.consumes.flow"),
          format = config.getString("data.consumes.format")
        ),
        produces = DataFlow(
          flow = config.getString("data.produces.flow"),
          format = config.getString("data.produces.format")
        )
      )
    )
  }

  def main(args: Array[String]): Unit = {

    val log = LoggerFactory.getLogger("DevLog")

    val parsedConfig = loadConfig()

    val in_file = "/home/marvin/workspace/data/endbpedia_sameAs.nt.sort.1kk"

    val cmd = parsedConfig.entry.replace("$IN_FILE", in_file).split(" ").toList
    val process = os.spawn(cmd = cmd.toSeq)


//    val l = Source.fromInputStream(process.stdout.wrapped).getLines().length
    process.waitFor()

    //    Thread.sleep(1000)
//    println(l.toString)
    println(process.exitCode().toString)
  }
}

