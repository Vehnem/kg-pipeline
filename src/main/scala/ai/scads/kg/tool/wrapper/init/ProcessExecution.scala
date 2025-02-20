package ai.scads.kg.tool.wrapper.init

import org.springframework.boot.CommandLineRunner
import org.springframework.stereotype.Component

@Component
class ProcessExecution(processManager: ProcessManager) extends CommandLineRunner {

  override def run(args: String*): Unit = {
    val thread = new Thread(new Runnable {
      override def run(): Unit = {
        while (true) {
          Thread.sleep(5000)
          val message = processManager.next()
          println("processed "+message.toString)
        }
      }
    })
    thread.start()
  }
}
