package ai.scads.kg.flex.frontier

object KGFlexAPI {

  var messageService: MessageService = null

  def execute(pipeline: Pipeline): Unit = {

    pipeline.stages.foreach({
      stage => executeStage(stage)
    })
  }

  def executeStage(stage: Stage): Unit = {
  }
}
