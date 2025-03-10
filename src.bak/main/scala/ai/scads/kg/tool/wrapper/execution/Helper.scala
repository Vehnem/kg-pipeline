package ai.scads.kg.tool.wrapper.execution

import org.apache.jena.rdf.model.ModelFactory
import org.apache.jena.vocabulary.RDF

import scala.sys.process._
import scala.util.matching.Regex

// A tiny model for demonstration
case class CliTool(
                    name: String,
                    version: Option[String],
                    options: List[CliOption]
                  )

//case class CliOption(
//                      shortFlag: Option[String],
//                      longFlag: Option[String],
//                      description: String
//                    )

// We'll store them in a small case class
case class CliOption(shortFlag: Option[String], longFlag: Option[String], description: String)

object CliHelpExtractor {

  def main(args: Array[String]): Unit = {
    // Example: We'll extract the help info for "git" (you can adapt for other tools)
    val toolName = "grep"
    val helpCommand = Seq(toolName, "--help")

    // 1. Execute the help command
    val helpOutput: String = helpCommand.!!
    println(s"Raw help output for $toolName:\n$helpOutput")

    // 2. Parse the output
    // A naive example: searching for lines that look like subcommands or options.
    // This part really depends on how the CLI formats its help text.
    val optionPattern: Regex = """(?i)^\s{0,2}(-\w, --\w+|\--\w+).*""".r
    // e.g. lines that start with -h, --help or --something



    // We'll iterate over each line, match the pattern, and parse out the short/long flags
    val cliOptions = helpOutput.split("\n").flatMap { line =>
      optionPattern.findFirstIn(line).map { matchedLine =>
        // For demonstration, let's split on whitespace or a dash pattern
        val tokens = matchedLine.trim.split("""\s+""")
        // This is simplistic: you'd refine according to the actual structure of the help text
        val (shortOpt, longOpt, desc) = parseOptions(tokens, line)
        CliOption(shortOpt, longOpt, desc)
      }
    }

    // 3. Print or store the extracted options
    cliOptions.foreach { opt =>
      println(s"ShortFlag: ${opt.shortFlag.getOrElse("")}, LongFlag: ${opt.longFlag.getOrElse("")}, Desc: ${opt.description}")
    }

    // 4. Build a basic knowledge graph structure (pseudo-code)
    // Suppose we have a simple model: CLI_Tool -> hasOption -> CLI_Option
    // For now, we just show an in-memory structure. You could convert to RDF, JSON-LD, Neo4j, etc.

    val gitTool = CliTool(name = toolName, version = None, options = cliOptions.toList)
    println("\nStructured representation:\n" + gitTool)

    val model = ModelFactory.createDefaultModel()

    val toolRes = model.createResource("http://example.org/tools/git")
    toolRes.addProperty(RDF.`type`, model.createResource("http://example.org/schema#CLI_Tool"))
    toolRes.addProperty(model.createProperty("http://example.org/schema#name"), "git")

    // Add each option
    gitTool.options.foreach { opt =>
      val optRes = model.createResource("http://example.org/tools/git/options/" + opt.longFlag.getOrElse(opt.shortFlag.getOrElse("unknown")))
      optRes.addProperty(RDF.`type`, model.createResource("http://example.org/schema#CLI_Option"))
      opt.shortFlag.foreach { sf =>
        optRes.addProperty(model.createProperty("http://example.org/schema#shortFlag"), sf)
      }
      opt.longFlag.foreach { lf =>
        optRes.addProperty(model.createProperty("http://example.org/schema#longFlag"), lf)
      }
      optRes.addProperty(model.createProperty("http://example.org/schema#description"), opt.description)

      toolRes.addProperty(model.createProperty("http://example.org/schema#hasOption"), optRes)
    }

    // Then you could write the model to Turtle, RDF/XML, JSON-LD, etc.

    model.write(System.out)
  }



  // A naive parser for the line tokens
  // The logic depends heavily on the actual CLI help format
  def parseOptions(tokens: Array[String], originalLine: String): (Option[String], Option[String], String) = {
    // Example tokens could be: ["-a,", "--all", "Commit", "all", "changes"]
    // We'll do a quick check:
    val short = tokens.find(_.startsWith("-") ).map(_.replaceAll("[,]", ""))  // remove trailing commas
    val long  = tokens.find(_.startsWith("--")).map(_.replaceAll("[,]", ""))

    // The rest is presumably description
    val descStartIndex = originalLine.indexOf(long.getOrElse(short.getOrElse("")))
    + long.getOrElse(short.getOrElse("")).length
    val desc = if(descStartIndex < originalLine.length) {
      originalLine.substring(descStartIndex).trim
    } else {
      ""
    }

    (short, long, desc)
  }


}
