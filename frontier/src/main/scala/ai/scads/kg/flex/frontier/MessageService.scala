package ai.scads.kg.flex.frontier

import org.springframework.amqp.rabbit.core.RabbitTemplate
import org.springframework.stereotype.Component

@Component
class MessageService(rabbitTemplate: RabbitTemplate) {

  import ai.scads.kg.core.Utils._

  def sendMessage(message: Any): Unit = {
    rabbitTemplate.convertAndSend(RabbitMqConfig.FANOUT_EXCHANGE,"",message.toJson)
  }
}
