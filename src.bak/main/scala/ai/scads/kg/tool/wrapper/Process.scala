package ai.scads.kg.tool.wrapper

import ai.scads.kg.core.driver.DDIMessage
import ch.qos.logback.core.sift.DefaultDiscriminator

abstract class Process {

  def run(message: DDIMessage): DDIMessage
}
