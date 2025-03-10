package ai.scads.kg.tool.wrapper.init

import ai.scads.kg.frontier.Message

import java.util.concurrent.Callable

abstract class Process(message: Message) extends Callable[Message] {

}

class CLIExecutionProcess(message: Message) extends Process(message) {

  override def call(): Message = {
    Thread.sleep(5000)
    Message("done","","","")
  }
}
