package ai.scads.kg.flex.frontier

case class Stage(process: String)

//embedded or on disk
case class Data(location: String)

//case class

case class Pipeline(input: String, output: String, dataDir: String, stages: List[Stage])
