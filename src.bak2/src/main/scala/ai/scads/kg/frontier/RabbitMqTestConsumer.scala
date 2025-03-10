package ai.scads.kg.frontier

import org.springframework.amqp.rabbit.annotation.RabbitListener
import org.springframework.stereotype.Component


@Component class RabbitMqTestConsumer {

  @RabbitListener(queues = Array("messageQueueDebug"))
  def receiveMessage(message: String): Unit = {
    System.out.println("Received message: " + message)
  }


  @RabbitListener(queues = Array("heartbeatQueue"))
  def receiveHeartbeat(message: String): Unit = {
    System.out.println("Received message: " + message)
  }
}
