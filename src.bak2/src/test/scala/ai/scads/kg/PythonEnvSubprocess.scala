package ai.scads.kg

import org.apache.commons.io.IOUtils
import org.scalatest.funsuite.AnyFunSuite

class PythonEnvSubprocess extends AnyFunSuite {


  test("run python env") {

    // Path to python env

    val proc = os.spawn(Seq("/usr/bin/env", "micromamba"))

    IOUtils.copy(proc.stdout.wrapped, System.out)
    proc.waitFor()

  }
}
