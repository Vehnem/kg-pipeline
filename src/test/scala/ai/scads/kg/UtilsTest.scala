package ai.scads.kg

import org.scalatest.funsuite.AnyFunSuite

class UtilsTest extends AnyFunSuite {

  test("case class json serialization") {

    case class Some(foo: String, bar: Int)
    case class Nest(more: List[Some])


    val some = Some("buz",0)
    val nest = Nest(List(some))

    import ai.scads.kg.tool.wrapper.Utils._

    val json = nest.toJson

//    val obje = json.fromJson[Nest]
//
//    println(obje)

  }

}
