package ai.scads.kg

import ai.scads.kg.Main.RegisterCLI
import picocli.CommandLine
import picocli.CommandLine.Command

import java.util.concurrent.Callable

object Main extends App {
  private val preparedArgs = if(args.length == 0) Array("-h") else args
  private val exitCode = new CommandLine(new Main()).execute(preparedArgs: _*)
  System.exit(exitCode)

  @Command(
    name="register",
    mixinStandardHelpOptions = true
  )
  class RegisterCLI extends Callable[Int]{

    // list, register/add, remove

    override def call(): Int = {

      0
    }
  }
}

@Command(
  name="dish",
  version = Array("v0.1"),
  subcommands = Array(classOf[RegisterCLI]),
  mixinStandardHelpOptions = true
)
class Main extends Callable[Int] {

  override def call(): Int = {
    0
  }
}