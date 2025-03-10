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

// Input needs an ID to identify batch data and window or event in stream

sealed trait ExchangeFormat{ val data: Array[Byte] }

case class NER()
case class NEL()
case class REL()
case class CoRef()
case class IEExchangeFormat(data: Array[Byte], ners: List[NER], nels: List[NEL], rels: List[REL], corefs: List[CoRef]) extends ExchangeFormat

case class Block(block_id: String, record_ids: List[String], block_key: String)
case class Match(pair_id: String, record_id1: String, record_id2: String, similarity: Float, features: Map[String,Float])
case class Cluster(cluster_id: String, member_record_ids: List[String])
case class Fusion()
case class ERExchangeFormat(data: Array[Byte], blocks: List[Block] , matches: List[Match], clusters: List[Cluster], fusions: List[Fusion]) extends ExchangeFormat