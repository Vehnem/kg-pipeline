package ai.scads.kg.core

import ai.scads.kg.core.model.{AnyFormat, BatchFlow, DataFlow}

import java.io.File

/**
 * tries to guess the source type and integrate as KG
 */
object DataSource {

  def fromFile(file: File): DataSource[File] = {
    new DataSource[File](file.getAbsolutePath)
  }
}

trait DataFlowFactory[T] {
  def create(uri: String): T
}

//class SomeDataFlow(val uri: String) extends DataFlow

class DataSource[T](uri: String) {

  def toData[F <: DataFlow, T](transformation: Function[T, F])
                              (implicit factory: DataFlowFactory[T]): DataFlow = {
    transformation.apply(factory.create(uri))
  }
}
