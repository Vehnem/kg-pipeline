package ai.scads.kg.tool.wrapper

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
    }

  }

}
