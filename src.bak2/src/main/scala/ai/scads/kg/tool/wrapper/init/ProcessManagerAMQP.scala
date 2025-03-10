package ai.scads.kg.tool.wrapper.init

import ai.scads.kg.frontier.Message
import org.springframework.amqp.core.{Binding, BindingBuilder, FanoutExchange, Queue}
import org.springframework.amqp.rabbit.annotation.RabbitListener
import org.springframework.amqp.rabbit.core.RabbitTemplate
import org.springframework.context.annotation.Bean
import org.springframework.stereotype.{Component, Service}

import java.util.concurrent.LinkedBlockingQueue
import scala.collection.mutable
import scala.jdk.CollectionConverters._

@Service
class ProcessManagerAMQP(rabbitTemplate: RabbitTemplate) extends ProcessManager {

  private val taskQueue = new LinkedBlockingQueue[Message]()

  @Bean
  def fanoutExchange: FanoutExchange = new FanoutExchange("messageFanout")

  @Bean def testQueue = new Queue("messageQueue", true) // true means durable

  @Bean def binding2(testQueue: Queue, fanoutExchange: FanoutExchange): Binding = BindingBuilder.bind(testQueue).to(fanoutExchange)

  @RabbitListener(queues = Array("messageQueue"))
  def receiveMessage(message: String): Unit = {
    import ai.scads.kg.tool.wrapper.Utils._
    System.out.println("Received message: " + message)
    addTasks(List(message.fromJson[Message]))
  }

  override def getTasks: List[Message] = {
    taskQueue.iterator().asScala.toList
  }

  override def addTasks(list: List[Message]): Unit = {
    taskQueue.addAll(list.asJava)
  }

  override def next(): Message = taskQueue.take()
}
