package ai.scads.kg.flex.frontier

import ai.scads.kg.core.Utils._
import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component
import picocli.CommandLine
import picocli.CommandLine.{Command, Parameters}

import java.util
import java.util.concurrent.Callable
import scala.io.{Source, StdIn}
import scala.jdk.CollectionConverters._

@Command(name = "kgflex", mixinStandardHelpOptions = true, subcommands = Array(classOf[KGFlexMonitor],classOf[KGFlexExecute]))
class KGFlexCLIMain extends Callable[Int] {

  override def call(): Int = {
    0
  }
}

@Command(name = "monitor")
class KGFlexMonitor() extends Callable[Int] {

  override def call(): Int = {
    StdIn.readLine()
    0
  }
}

@Command(name = "execute")
class KGFlexExecute() extends Callable[Int] {

  @Parameters
  var params: util.ArrayList[String] = new util.ArrayList[String]()

  override def call(): Int = {


    val filePath = params.asScala.head
    val fileSource = Source.fromFile(filePath)
    val fileContent = fileSource.getLines().mkString("\n")

    val pipeline = fileContent.fromJson[Pipeline]

    KGFlexAPI.execute(pipeline)
    0
  }
}

@Component
class KGFlexCLI extends CommandLineRunner {

  override def run(args: String*): Unit = {
    val cli =  new CommandLine(classOf[KGFlexCLIMain])
    if(args.isEmpty)
      cli.execute("--help")
    else
      cli.execute(args: _*)
  }
}
