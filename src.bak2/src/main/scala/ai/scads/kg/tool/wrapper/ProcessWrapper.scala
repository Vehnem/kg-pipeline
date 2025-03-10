package ai.scads.kg.tool.wrapper

import org.springframework.stereotype.Component

@Component
abstract class ProcessWrapper {

  def process(messageTemplate: MessageTemplate): MessageTemplate

}
