package ai.scads.kg.tool.wrapper.execution

import org.apache.commons.io.IOUtils

import java.io.{ByteArrayInputStream, DataInput, DataInputStream, File, FileInputStream, FileOutputStream, InputStream, OutputStream}
import java.time.Duration
import scala.io.Source

trait Execution {

}
//  def call(cmd: Seq[String], in: Option[InputStream] = None, out: Option[OutputStream] = None): ExecutionReport
//}
//
case class ExecutionReport(val cmd: String, val exitCode: Int, val duration: Long) {

  override def toString: String = s"Cmd: $cmd, ExitCode: $exitCode, Duration: ${Duration.ofMillis(duration)}"
}


class CmdTemplate {

}

class CliExecution extends Execution {

  def call(cmd: Seq[String],
           inputFile: Option[File] = None,
           outputFile: Option[File] = None,
           inputStream: Option[InputStream] = None,
           outputStream: Option[OutputStream] = None,
           inputFlag: Option[String] = None,
           outputFlag: Option[String] = None
          ): ExecutionReport = {

    val startTime = System.currentTimeMillis()
    var skipNext = false  // Track flag + placeholder removal

    val finalCmd = cmd.zipWithIndex.flatMap {
      // Remove input flag and placeholder if using stdin
      case (flag, _) if inputFile.isEmpty && inputStream.isDefined && inputFlag.contains(flag) =>
        skipNext = true  // Skip the placeholder too
        Seq()

      case ("<INPUT_FILE>", _) if skipNext =>
        skipNext = false
        Seq()

      // Remove output flag and placeholder if using stdout
      case (flag, _) if outputFile.isEmpty && outputStream.isDefined && outputFlag.contains(flag) =>
        skipNext = true  // Skip the placeholder too
        Seq()

      case ("<OUTPUT_FILE>", _) if skipNext =>
        skipNext = false
        Seq()

      // Replace input file placeholder
      case ("<INPUT_FILE>", _) if inputFile.isDefined =>
        Seq(inputFile.get.getAbsolutePath)

      // Replace output file placeholder
      case ("<OUTPUT_FILE>", _) if outputFile.isDefined =>
        Seq(outputFile.get.getAbsolutePath)

      // Keep other command parts unchanged
      case (arg, _) =>
        Seq(arg)
    }

//    val inStream = inputFile.map(new FileInputStream(_)).orElse(inputStream)
//    val outStream = outputFile.map(new FileOutputStream(_)).orElse(outputStream)

    val logValue = new StringBuilder()
    if(inputStream.isDefined) logValue.append("..| ")
    logValue.append(finalCmd.mkString(" "))
    if(outputStream.isDefined) logValue.append(" |..")

    val process = inputStream match {
      case Some(in) => os.spawn(cmd = finalCmd, stdin = in)
      case None     => os.spawn(cmd = finalCmd)
    }

    if (outputStream.isDefined) {
      IOUtils.copy(process.stdout.wrapped, outputStream.get)
    } else {
      process.waitFor()
    }

    val duration = System.currentTimeMillis() - startTime
    ExecutionReport(logValue.toString(), exitCode = process.exitCode(), duration = duration)
  }
}

class CommandTemplateBuilder(baseCmd: Seq[String]) {
  private var args: Seq[String] = Seq()
  private var options: Map[String, Option[String]] = Map()
  private var inputFlag: Option[String] = None  // Flag used for input file
  private var outputFlag: Option[String] = None // Flag used for output file

  /** Add a positional argument */
  def argument(arg: String): CommandTemplateBuilder = {
    args = args :+ arg
    this
  }

  /** Add an option flag */
  def option(flag: String, value: Option[String] = None): CommandTemplateBuilder = {
    options += (flag -> value)
    this
  }

  /** Define that a flag should be replaced with the input file */
  def input(flag: Option[String]): CommandTemplateBuilder = {
    inputFlag = flag
    this
  }

  /** Define that a flag should be replaced with the output file */
  def output(flag: Option[String]): CommandTemplateBuilder = {
    outputFlag = flag
    this
  }

  /** Builds the command, removing flags if no file is provided */
  def build(): CommandTemplate = {
    val optionsSeq = options.flatMap {
      case (flag, Some(value)) => Seq(flag, value)
      case (flag, None) => Seq(flag)
    }.toSeq

    val cmdWithPlaceholders = baseCmd ++ optionsSeq ++ args ++
      inputFlag.map(flag => Seq(flag, "<INPUT_FILE>")).getOrElse(Seq()) ++
      outputFlag.map(flag => Seq(flag, "<OUTPUT_FILE>")).getOrElse(Seq())

    CommandTemplate(cmdWithPlaceholders, inputFlag, outputFlag)
  }
}


object CommandTemplateBuilder {
  def apply(baseCmd: String*): CommandTemplateBuilder = new CommandTemplateBuilder(baseCmd)
}

case class CommandTemplate(
                            cmd: Seq[String],
                            inputFlag: Option[String],
                            outputFlag: Option[String]
                          ) {
  def execute(inputFile: Option[File] = None, outputFile: Option[File] = None,
              inputStream: Option[InputStream] = None, outputStream: Option[OutputStream] = None)
             (implicit executor: CliExecution): ExecutionReport = {

    executor.call(cmd, inputFile, outputFile, inputStream, outputStream, inputFlag, outputFlag)
  }
}


//class HttpApiExecution extends Execution {
//
//
//}
//
//class WebServerExecution extends Execution {
//
//}


object Execution extends App {

  implicit val cliExecutor: CliExecution = new CliExecution

  val grepCmd = CommandTemplateBuilder("grep")
    .argument("error")
    .option("-i")
    .input(Some(""))
    .build()

  val inputData = "INFO: No issues\nERROR: exception occurred\nDEBUG: running..."
  val inputStream = new ByteArrayInputStream(inputData.getBytes)

  val report = grepCmd.execute(
    inputFile = Some(new File("grep.out")),
//    outputFile = Some(new File("grep.out")),
//    inputStream = Some(inputStream),
    outputStream = Some(System.out)
  )

  println(report)
}