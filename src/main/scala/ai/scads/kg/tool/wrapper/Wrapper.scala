package ai.scads.kg.tool.wrapper

//import ai.scads.kg.Data

case class Message()

trait Wrapper {

  def execute(message: Message): Message
}


