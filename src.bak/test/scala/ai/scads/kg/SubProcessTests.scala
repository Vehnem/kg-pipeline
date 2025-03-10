package ai.scads.kg

import org.scalatest.funsuite.AnyFunSuite
import os._

import java.io.PrintWriter
import java.time.Duration

class SubProcessTests extends AnyFunSuite {

  // TODO benchmark...
  test("main subprocesstest") {
    val start = System.nanoTime()
    val sub = os.spawn(cmd = ("bash", "src/main/shell/echo.sh", "arg1", "arg2"))
    val lines = sub.stdout.lines()
    val end = System.nanoTime()
    println("lines count "+lines.length)
    lines.foreach(println)
    println(Duration.ofNanos(end-start))
  }

  test("grep") {

  }
}
