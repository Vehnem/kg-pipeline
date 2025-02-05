package ai.scads.kg.core.model

import scala.annotation.StaticAnnotation
import scala.reflect.runtime.universe
import scala.reflect.runtime.universe._

// Define the annotation
class statement extends StaticAnnotation

// Define the MetaEntity trait
trait MetaEntity {

  val id: String

  def toStatement: List[(String,String,String)] = {
    val mirror = runtimeMirror(this.getClass.getClassLoader)
    val instanceType = mirror.classSymbol(this.getClass).toType

    val fields = instanceType.members.collect {
      case m: MethodSymbol if m.isGetter =>
        println(m)
        m
    }

    val statements = fields.flatMap { field =>
      val fieldName = field.name.toString
      val fieldValue = mirror.reflect(this).reflectMethod(field.asMethod)()

      if (field.annotations.exists(_.tree.tpe =:= typeOf[statement])) {
        fieldValue match {
          case _: Function1[_, _] => Some((id, fieldName, field.asMethod.paramLists.flatten.map(_.name).mkString(", ")))
          case _ => Some((id, fieldName, fieldValue.toString))
        }
      } else {
        None
      }
    }

    val constructor = instanceType.decl(termNames.CONSTRUCTOR).asMethod
    val constructorParams = constructor.paramLists.flatten
    val instanceMirror = mirror.reflect(this)

    val statements2 = constructorParams.flatMap { param =>
      val paramName = param.name.toString
      val paramValue = instanceMirror.reflectField(instanceType.decl(param.name).asTerm).get

      param.annotations.find(_.tree.tpe =:= universe.typeOf[statement]).flatMap[(String,String,String)] { annotation =>
        annotation.tree.children.tail.collectFirst {
          case any =>
            print("h")
//          case universe.Literal(universe.Constant(customName: String)) =>
          (id, paramName, paramValue.toString)
        }
      }
    }

    (statements ++ statements2).toList

//    (statements ++ statements2) mkString(", ")
  }
}

// Example case class using the MetaEntity trait
case class ExampleEntity(id: String, @statement name: String, age: Int, @statement f: (Int => String)) extends MetaEntity

// Example usage
object ShortTest extends App {
  val entity = ExampleEntity("some","Alice", 25, (x: Int) => s"Number: $x")
  println(entity.toStatement) // Should print "name: Alice, f(x)"
}
