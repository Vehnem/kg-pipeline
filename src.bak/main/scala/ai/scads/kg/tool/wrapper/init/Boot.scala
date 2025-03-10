package ai.scads.kg.tool.wrapper.init

import ai.scads.kg.frontier.Message
import org.springframework.amqp.core.{Binding, BindingBuilder, FanoutExchange, Queue}
import org.springframework.amqp.rabbit.annotation.RabbitListener
import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.context.annotation.Bean
import org.springframework.stereotype.Component

@SpringBootApplication
class Boot {

}

object Boot extends App {
  SpringApplication.run(classOf[Boot], args: _*)
}
