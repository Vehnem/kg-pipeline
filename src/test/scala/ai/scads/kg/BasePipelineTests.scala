package ai.scads.kg

import ai.scads.kg.core.DataSource
import ai.scads.kg.core.model.{AnyFormat, BatchFlow}
import org.scalatest.funsuite.AnyFunSuite

import java.io.File
import scala.io.Source

class BasePipelineTests extends AnyFunSuite {

  test("DBpedia Abstract Extraction") {

  }

  test("Data Source") {

    val file = "src/resource/input/some.txt"

    val flow = DataSource.fromFile(new File(file)).toData({
      f =>
        val s = Source.fromFile(f)
        try  {
          s.getLines()
          new BatchFlow[AnyFormat] {}
        } finally {
          s.close()
        }
    })
  }
}
