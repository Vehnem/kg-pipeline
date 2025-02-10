package ai.scads.kg.core.driver

import java.io.Serializable

trait TransformationFunction extends Serializable {
  def transform(data: Seq[String]): Seq[String]
}

// Example transformation: uppercase
class UppercaseTransformation extends TransformationFunction {
  override def transform(data: Seq[String]): Seq[String] =
    data.map(_.toUpperCase)
}
