package ai.scads.kg.frontier

import com.fasterxml.jackson.annotation.JsonSubTypes
import com.fasterxml.jackson.annotation.JsonTypeInfo

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes(Array(
  new JsonSubTypes.Type(value = classOf[Heartbeat], name = "Heartbeat"),
  new JsonSubTypes.Type(value = classOf[DataUpdate], name = "DataUpdate")
))
sealed trait RabbitMessage

case class Heartbeat(timestamp: Long) extends RabbitMessage
case class DataUpdate(id: String, value: Int) extends RabbitMessage

case class Message(task: String, input: String, output: String, timestamp: String)
