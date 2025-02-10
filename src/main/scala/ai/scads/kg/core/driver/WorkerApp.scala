package ai.scads.kg.core.driver
import java.io._
import java.net._

import java.io._
import java.net._

object WorkerApp extends App {
  val workerPort = 5001
  val serverSocket = new ServerSocket(workerPort)
  println(s"Worker started on port $workerPort, waiting for tasks...")

  while (true) {
    val clientSocket = serverSocket.accept()

    // Because the Master is the one writing first, the Worker must read first
    val in  = new ObjectInputStream(clientSocket.getInputStream)
    val out = new ObjectOutputStream(clientSocket.getOutputStream)

    try {
      // 1) Read data from the Master
      val chunkId       = in.readInt()
      val data          = in.readObject().asInstanceOf[Seq[String]]
      val transformation= in.readObject().asInstanceOf[TransformationFunction]

      println(s"Worker received chunk $chunkId: $data")

      // 2) Apply transformation
      val processedData = transformation.transform(data)

      // 3) Send results back to the Master
      out.writeInt(chunkId)
      out.writeObject(processedData)
      out.flush()

    } catch {
      case eof: EOFException =>
        println(s"EOFException while reading: ${eof.getMessage}")
      case e: Exception =>
        e.printStackTrace()
    } finally {
      clientSocket.close()
    }
  }
}
