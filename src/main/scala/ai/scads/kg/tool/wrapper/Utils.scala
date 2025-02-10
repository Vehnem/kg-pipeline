package ai.scads.kg.tool.wrapper

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import com.fasterxml.jackson.core.`type`.TypeReference

import java.io.StringWriter

// switch to upickle
object Utils {

  val mapper = new ObjectMapper()
  mapper.registerModule(DefaultScalaModule)

  implicit class ImplicitConversions[T](val any: T) {
    def toJson: String = {
      val out = new StringWriter
      mapper.writeValue(out, any)
      out.toString
    }
  }

  implicit class JsonParser(val string: String) {
    def fromJson[T](implicit m: Manifest[T]): T = {
      mapper.readValue(string, new TypeReference[T] {
        override def getType = m.runtimeClass
      })
    }
  }
}

