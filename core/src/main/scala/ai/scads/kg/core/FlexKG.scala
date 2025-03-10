package ai.scads.kg.core

class FlexKG {

  def buildPipeline(): Unit = {}

  class Stage() {
    def invoke: Unit = {

      // send message to trigger
      // monitor and wait for message

    }
  }

  class Pipeline(stages: List[Stage]) {

    def run(): Unit = {

      stages.foreach({
        stage =>
          stage.invoke
      })
    }
  }


}
