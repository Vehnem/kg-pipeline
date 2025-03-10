package ai.scads.kg.frontier

import ai.scads.kg.tool.wrapper.Utils
import com.rabbitmq.client.ConnectionFactory
import org.springframework.amqp.core.{AmqpAdmin, FanoutExchange}
import org.springframework.amqp.rabbit.core.{RabbitAdmin, RabbitTemplate}
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.context.annotation.Bean
import org.springframework.web.bind.annotation.{GetMapping, RequestMapping, RestController}

import java.time.Instant

@SpringBootApplication
class FrontierBoot {


//  @Bean def rabbitAdmin(connectionFactory: ConnectionFactory) = new RabbitAdmin(connectionFactory)
//  @Bean def cf1: ConnectionFactory =  new ConnectionFactory()

  @RestController
  @RequestMapping(value = Array("/"))
  class MainController(rabbitTemplate: RabbitTemplate, amqpAdmin: AmqpAdmin) {

//    private val

//    @Value("${rabbitmq.test.queue}")
//    private val testQueue = null

    @GetMapping(value = Array("foo"))
    def foo(): Unit = {
      println("doing")
    }

    @GetMapping(value = Array("purge"))
    def purgeQueues(): Unit = {
      amqpAdmin.purgeQueue("messageQueue")
    }

    @GetMapping(value = Array("publish"))
    def publish(): Unit = {
      import Utils._
      rabbitTemplate.convertAndSend("messageFanout","",Message("t1","in","out", Instant.now().toString).toJson)
    }
  }
}

object FrontierBoot extends App {
  System.setProperty("server.port","9999")
  SpringApplication.run(classOf[FrontierBoot], args: _*)
}