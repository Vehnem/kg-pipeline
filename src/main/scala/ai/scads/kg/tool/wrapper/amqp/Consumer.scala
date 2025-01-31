package ai.scads.kg.tool.wrapper.amqp

import org.springframework.stereotype.Component

import java.util.concurrent.CountDownLatch

@Component
class Consumer {
  val latch = new CountDownLatch(1)

  def receiveMessage(message: String): Unit = {
    System.out.println("Received <" + message + ">")
    latch.countDown()
  }
}
