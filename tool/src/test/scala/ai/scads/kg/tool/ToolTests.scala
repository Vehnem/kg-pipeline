//package ai.scads.kg.tool
//
//import ai.scads.kg.tool.FlexKGToolAPI.{KGFlexProcess, KGFlexProcessMessage, ProcessType}
//import org.scalatest.funsuite.AnyFunSuite
//
//class ToolTests extends AnyFunSuite {
//
//  test("echo script.sh execution") {
//
//    val proc = new KGFlexProcess {
//
//      override val processType: ProcessType = ProcessType.EntityResolution
//
//      override def exec(message: FlexKGToolAPI.KGFlexProcessMessage): FlexKGToolAPI.ExecutionReport = {
//        val start = System.nanoTime()
//        val outFile =  os.pwd / message.output.head
//        val proc = os.call(Seq("/usr/bin/bash","src/main/shell/echo.sh",message.input.head,message.output.head),stdout = outFile)
//        FlexKGToolAPI.ExecutionReport(proc.exitCode,System.nanoTime()-start,message)
//      }
//    }
//    val exrep = proc.exec(KGFlexProcessMessage(0,List("path/to/some/file"),List("target/outfile.txt")))
//
//    println(exrep)
//  }
//}
