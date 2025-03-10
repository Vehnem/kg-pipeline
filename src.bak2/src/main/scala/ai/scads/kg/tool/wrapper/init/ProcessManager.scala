package ai.scads.kg.tool.wrapper.init

import ai.scads.kg.frontier.Message

trait ProcessManager {

  def getTasks: List[Message]

  def addTasks(list: List[Message]): Unit

  def next(): Message
}
