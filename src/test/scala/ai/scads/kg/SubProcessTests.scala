package ai.scads.kg

import org.scalatest.funsuite.AnyFunSuite
import os._

import java.io.PrintWriter

class SubProcessTests extends AnyFunSuite {

  test("main subprocesstest") {
    val sub = os.spawn(cmd = ("ls", "-lh", "."))
    val len = sub.stdout.lines().length

  }

  test("grep") {

  }
}
