package ai.scads.kg.flex.frontier

import ai.scads.kg.flex.frontier.RabbitMqConfig.{FANOUT_EXCHANGE, HEARTBEAT_QUEUE, PROCESS_QUEUE_DEBUG}
import org.springframework.amqp.core.{Binding, BindingBuilder, FanoutExchange, Queue}
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter
import org.springframework.context.annotation.{Bean, Configuration}

object RabbitMqConfig {

  final val FANOUT_EXCHANGE = "messageFanout"
  final val PROCESS_QUEUE_DEBUG = "messageQueueDebug"
  final val PROCESS_QUEUE = "messageQueue"
  final val HEARTBEAT_QUEUE = "heartbeatQueue"
}

@Configuration
class RabbitMqConfig {

  @Bean
  def fanoutExchange: FanoutExchange = new FanoutExchange(FANOUT_EXCHANGE)

  @Bean def testQueue = new Queue(PROCESS_QUEUE_DEBUG, true) // true means durable

  @Bean def binding2(testQueue: Queue, fanoutExchange: FanoutExchange): Binding = BindingBuilder.bind(testQueue).to(fanoutExchange)

  @Bean def heartbeatQueue = new Queue(HEARTBEAT_QUEUE, true)

  @Bean def messageConverter = new Jackson2JsonMessageConverter()
}