package ai.scads.kg.tool.wrapper.execution

import org.apache.commons.io.IOUtils

import java.io.{DataInput, DataInputStream, File, FileInputStream}

trait Execution {

}


class CliExecution extends Execution {

}

class HttpApiExecution extends Execution {

}

class WebServerExecution extends Execution {

}

object Execution extends App {


  val inFilePath = "/home/marvin/paper/kgpipeline/kg-pipeline/experiments/pipeline/source.nt"

  // send stdin capture stdout

  val is = new FileInputStream(new File(inFilePath))

  val proc = os.spawn(cmd = Seq("/usr/bin/env","bash","kg-tools/_echo/cli/echo_stdin_stdout.sh"),stdin = is)
DataInputStream
  DataInput

  proc.stdout.data


}