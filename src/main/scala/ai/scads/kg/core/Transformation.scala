package ai.scads.kg.core

import ai.scads.kg.Data

abstract class Transformation[A <: Data, B <: Data](source: A, target: B, supplementIn: Data, supplementOut: Data) {

  // TODO Runnable?
  def transform(): Unit


  trait Foobar {
    val config: String
    val data: String

    def buz = config + data
  }

//  def processFoobar(foobar: Foobar): String = {
//
//  }

  def run(): Unit = {

    def something(f: Foobar => String): String = {
      ""
    }

//    something(new Foobar {
//      val config = ""
//      val data = ""
//    })

  }
}