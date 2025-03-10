package ai.scads.kg.core

case class Data(flow: String, format: String, location: String)

/*{
  "task": "EntityResolution",
  "accept": "EntityResolutionOut",
  "input": {
    "format": "",
    "flow": "batch",
    "location": "foo/bar"
  }
}*/
case class Task(input: Data, key: String)


case class TaskReport(
                            processCode: Long,
                            durationNano: Long,
                            message: Task
                     )