package ai.scads.kg.core.interfaces

import java.io.File
import java.net.URLClassLoader
import scala.reflect.runtime.universe


// Plugin system
object PluginLoader {
  private var registry = Map[String, Any]()

  def loadPlugins(jarPath: String): Unit = {
    val jarFile = new File(jarPath)
    val classLoader = new URLClassLoader(Array(jarFile.toURI.toURL), this.getClass.getClassLoader)
    val mirror = universe.runtimeMirror(classLoader)

    jarFile.listFiles(_.getName.endsWith(".class")).foreach { file =>
      val className = file.getName.stripSuffix(".class")
      val module = mirror.staticModule(className)
      val obj = mirror.reflectModule(module).instance
      registry += (className -> obj)
    }
  }

  def getPlugin(name: String): Option[Any] = registry.get(name)

  def main(args: Array[String]): Unit = {
    // Load plugins from a jar
    PluginLoader.loadPlugins("path/to/plugin.jar")
    val pluginInstance = PluginLoader.getPlugin("MyPlugin")
    println(pluginInstance)
  }
}