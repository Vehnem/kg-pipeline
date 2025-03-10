package ai.scads.kg.tool

import org.springframework.amqp.rabbit.annotation.RabbitListener
import org.springframework.stereotype.{Component, Service}

object FlexKGToolAPI {

  /**
   *
   */
  case class KGFlexProcessMessage(
                    id: Long,
                    input: List[String],
                    output: List[String]
                    )

  @Service
  class KGFlexMessageConsumer(process: KGFlexProcess) {

    @RabbitListener(queues = Array("messageQueueDebug"))
    def receiveMessage(message: String): Unit = {
      import ai.scads.kg.Utils._
      System.out.println("Received message: " + message)
      process.exec(message.fromJson[KGFlexProcessMessage])
    }

    def consume() : Unit = {

      val message = KGFlexProcessMessage(0, List(), List())
    }
  }

  // Entity for data io
  // Payload
  // Configs
  // Supplements
  trait DataEntity {

  }

  @Component
  trait KGFlexProcess {

    val processType: ProcessType

    def exec(message: KGFlexProcessMessage) : ExecutionReport
  }

  object ProcessType {

    val EntityResolution: ProcessType = "EntityResolution"
    val InformationExtraction: ProcessType = "InformationExtraction"
    val Refinement: ProcessType = "Refinement"
//    val DataCleaning: ProcessType = ""
  }

  type ProcessType = String


  case class ExecutionReport(
                              processCode: Long,
                              durationNano: Long,
                              message: KGFlexProcessMessage
                            )

  /**
   * Maybe be a Callable
   */
  trait Execution {

    def exec(): ExecutionReport
  }

//  class HttpExecution extends Execution {

//    override def exec(): ExecutionReport = ExecutionReport()
//  }

//  class CliExecution extends Execution {

//    override def exec(): ExecutionReport = {
//      //
//      ExecutionReport()
//    }
//  }

}