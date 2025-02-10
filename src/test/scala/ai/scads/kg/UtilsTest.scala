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

    val obje = json.fromJson[Nest]
//
    println(obje)

  }


//  test("os env test"){
//
//    os.spawn()
//  }

//  object ShortTest extends App {
//
//    implicit class IteratorOps(it1: Iterator[String]) {
//      def +*(it2: Iterator[String]): Iterator[String] = new Iterator[String] {
//        override def hasNext: Boolean = it1.hasNext || it2.hasNext
//
//        override def next(): String = {
//          if (it1.hasNext && (!it2.hasNext || (it1.hasNext && it2.hasNext && !toggle))) {
//            toggle = !toggle
//            it1.next()
//          } else {
//            toggle = !toggle
//            it2.next()
//          }
//        }
//
//        private var toggle: Boolean = false
//      }
//    }
//
//    // Example usage:
//    val it1 = Iterator("A1", "A2", "A3")
//    val it2 = Iterator("B1", "B2", "B3", "B4")
//
//    val merged = it1 +* it2
//    merged.foreach(println)
//
//  }

}
