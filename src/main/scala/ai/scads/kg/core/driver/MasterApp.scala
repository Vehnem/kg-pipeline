package ai.scads.kg.core.driver
import java.io._
import java.net._
import scala.concurrent._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.util.{Failure, Success}
import java.io._
import java.net._
import scala.concurrent._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.DurationInt
import scala.util.{Failure, Success}

object MasterApp extends App {
  // List of worker IPs/ports. Adjust if you have multiple workers.
  val workers = Seq("127.0.0.1" -> 5001)

  // Data to process
  val data = Seq("hello", "world", "distributed", "computing", "scala", "sockets")

  // Our transformation function
  val transformation = new UppercaseTransformation()

  // Split data into chunks (one chunk per worker, or more, as needed)
  val chunkSize = math.max(1, data.length / workers.length)
  val chunks    = data.grouped(chunkSize).zipWithIndex.toList

  val futures = chunks.map { case (chunk, chunkId) =>
    val (workerHost, workerPort) = workers(chunkId % workers.length)

    Future {
      // Connect to the worker
      val socket = new Socket(workerHost, workerPort)

      // Because Master is the first to write, create ObjectOutputStream first
      val out = new ObjectOutputStream(socket.getOutputStream)
      out.flush()  // Ensures the header is sent
      val in  = new ObjectInputStream(socket.getInputStream)

      // 1) Send the chunk
      out.writeInt(chunkId)
      out.writeObject(chunk)
      out.writeObject(transformation)
      out.flush()

      // 2) Read the processed result
      val resultChunkId = in.readInt()
      val result        = in.readObject().asInstanceOf[Seq[String]]

      socket.close()
      (resultChunkId, result)
    }
  }

  val finalFuture = Future.sequence(futures)

  // Block until everything is done or a timeout occurs
  try {
    val results = Await.result(finalFuture, 30.seconds)
    // or Duration.Inf if you never want a timeout
    val finalData = results.sortBy(_._1).flatMap(_._2)
    println(s"Final Processed Data: $finalData")
  } catch {
    case e: Exception =>
      println(s"Error waiting for results: ${e.getMessage}")
  }

//  // Gather all results asynchronously
//  Future.sequence(futures).onComplete {
//    case Success(results) =>
//      // Sort by chunkId and flatten
//      val finalData = results.sortBy(_._1).flatMap(_._2)
//      println(s"Final Processed Data: $finalData")
//
//    // You might want to System.exit(0) or keep the program running
//    case Failure(e) =>
//      println(s"Error occurred: ${e.getMessage}")
//  }

  println("DONE")
}

