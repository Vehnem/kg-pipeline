package ai.scads.kg.tool.wrapper

import ai.scads.kg.Data

trait Wrapper {

  def execute(config: Any): List[Data]
}


class CliWrapper extends Wrapper {

  override def execute(config: Any): List[Data] = {

    List()
  }
}

class ApiWrapper {

}

object Wrapper {

}

