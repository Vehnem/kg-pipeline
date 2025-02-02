package ai.scads.kg

import org.scalatest.funsuite.AnyFunSuite
import os._

import java.io.PrintWriter

class SubProcessTests extends AnyFunSuite {

  test("main subprocesstest") {
    val sub = os.spawn(cmd = ("ls", "-lh", "."))
    sub.stdout.lines().foreach(println)

//    val os = result
//    println(result.out.)
//    println(os.proc("ls", "-lh", ".").call().out.chunks.foreach(println))

    println("lo")
  }
}
