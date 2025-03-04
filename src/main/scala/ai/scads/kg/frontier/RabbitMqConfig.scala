package ai.scads.kg.frontier

import org.springframework.amqp.core.{Binding, BindingBuilder, FanoutExchange, Queue}
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter
import org.springframework.context.annotation.{Bean, Configuration}

@Configuration
class RabbitMqConfig {

  @Bean
  def fanoutExchange: FanoutExchange = new FanoutExchange("messageFanout")

  @Bean def testQueue = new Queue("messageQueueDebug", true) // true means durable

  @Bean def binding2(testQueue: Queue, fanoutExchange: FanoutExchange): Binding = BindingBuilder.bind(testQueue).to(fanoutExchange)

  @Bean def heartbeatQueue = new Queue("heartbeatQueue", true)

  @Bean def messageConverter = new Jackson2JsonMessageConverter()
}