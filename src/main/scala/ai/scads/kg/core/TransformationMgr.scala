package ai.scads.kg.core

import ai.scads.kg.Data

import scala.collection.mutable

class TransformationMgr {

  private val functionMap = new mutable.HashMap[String,Data => Data]()

  def register(f: Data => Data): Unit = {
//    functionMap("").apply()
  }

  def get(): Unit = {

  }

}
