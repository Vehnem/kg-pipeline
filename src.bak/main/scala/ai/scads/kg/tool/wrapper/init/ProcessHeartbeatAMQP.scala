package ai.scads.kg.tool.wrapper.init

import org.springframework.amqp.core.Queue
import org.springframework.amqp.rabbit.core.RabbitTemplate
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.CommandLineRunner
import org.springframework.context.annotation.Bean
import org.springframework.stereotype.Component

@Component
class ProcessHeartbeatAMQP(processManager: ProcessManager, rabbitTemplate: RabbitTemplate) extends CommandLineRunner{

  @Value("${heartbeat.interval:10000}")
  var heartbeatInterval : Long = _

  @Bean def heartbeatQueue = new Queue("heartbeatQueue", true)

  override def run(args: String*): Unit = {
    val thread = new Thread(new Runnable {
      override def run(): Unit =
        while (true) {
          Thread.sleep(heartbeatInterval)
          import ai.scads.kg.tool.wrapper.Utils._
          val message = processManager.getTasks.toJson
          rabbitTemplate.convertAndSend("heartbeatQueue",message)
        }
    })
    thread.start()
  }
}
