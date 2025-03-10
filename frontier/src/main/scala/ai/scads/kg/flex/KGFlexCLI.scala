package ai.scads.kg.flex

import picocli.CommandLine
import picocli.CommandLine.{Command, Option, Parameters}

import java.util.concurrent.Callable
import java.util

import scala.jdk.CollectionConverters._

@Command(name = "kgflex", mixinStandardHelpOptions = true, subcommands = Array(classOf[KGFlexExecute]))
class KGFlexCLI extends Callable[Int] {

  override def call(): Int = {
    0
  }
}

@Command(name = "execute")
class KGFlexExecute() extends Callable[Int] {

  @Parameters
  var params: util.ArrayList[String] = new util.ArrayList[String]()

  override def call(): Int = {

    params.asScala.foreach(println)
    0
  }
}

object KGFlexCLI extends App {

  val cli =  new CommandLine(classOf[KGFlexCLI])
  if(args.length == 0)
    cli.execute("--help")
  else
    cli.execute(args: _*)
}
