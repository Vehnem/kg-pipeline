package ai.scads.kg

import ai.scads.kg.core.DataSource
import ai.scads.kg.core.model.{AnyFormat, BatchFlow}
import org.scalatest.funsuite.AnyFunSuite

import java.io.{File, FileFilter}
import scala.io.Source

class BasePipelineTests extends AnyFunSuite {

  type FilePath = String

  /*
  /home/marvin/workspace/papers/vldb/data/dbpedia-abs/data/en
  *.txt
  *.json
  *.csv
   */

  object Ops {
    implicit class PipelineOps(array: Array[ExchangeFormat]) {

      def agg(f: String => String): KG = {
        array.map(ex => f.apply(ex.meta)).mkString
      }
    }
  }

  type KG = String
  type ExchangeData = String
  case class ExchangeFormat(file: File, meta: String)

  test("pipeline") {
    import Ops._

    val sourceFilePath = java.nio.file.Paths.get("/home/marvin/workspace/papers/vldb/data/dbpedia-abs/data/en")
    val sourceFile = sourceFilePath.toFile
    val textFiles = sourceFile.listFiles(new FileFilter {
      override def accept(pathname: File): Boolean = {
        pathname.toString.endsWith("*.txt")
      }
    })
    textFiles.map({
      textFile =>
        executeOpenIE(textFile)
      // OpenIE
      // Falcon2.0
    }).map({
      exchangeFormat =>
        executeFalcon2(exchangeFormat.file)
    }).agg({
      format =>
        ""
    })
  }


  def executeOpenIE(file: File): ExchangeFormat = {
    ExchangeFormat(file, "")
  }

  def executeFalcon2(file: File): ExchangeFormat = {
    ExchangeFormat(file,"")
  }


//  test("DBpedia Abstract Extraction") {
//
//  }

//  test("Data Source") {
//
//    val file = "src/resource/input/some.txt"
//
//    val flow = DataSource.fromFile(new File(file)).toData({
//      f =>
//        val s = Source.fromFile(f)
//        try  {
//          s.getLines()
//          new BatchFlow[AnyFormat] {}
//        } finally {
//          s.close()
//        }
//    })
//  }
}
