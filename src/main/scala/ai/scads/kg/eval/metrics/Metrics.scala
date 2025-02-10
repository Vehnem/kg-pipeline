package ai.scads.kg.eval.metrics

import scala.collection.mutable.ListBuffer

trait Metric {

  val reports = new ListBuffer[String]()

  def eval(a: Any, b: Any): MetricResult

}

trait MetricResult

object Metrics {
  // TODO Overlap between A and B

  class Coverage extends Metric {

    def eval(a: Any, b: Any): MetricResult = {

      new MetricResult {}
    }
  }

//  class Succinctness extends Metric
//  class Completeness extends Metric

}
