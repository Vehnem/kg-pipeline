package ai.scads.kg.core

import org.apache.commons.io.IOUtils

import java.io.ByteArrayInputStream
import scala.concurrent._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.io.Source
import scala.util.{Failure, Success}

object Processing {

  def mapAsync[A, B](parallel: Int, iterator: Iterator[A], f: A => B): Iterator[Future[B]] = {
    // Create a fixed thread pool for parallel execution
    implicit val ec: ExecutionContextExecutor = ExecutionContext.fromExecutor(
      java.util.concurrent.Executors.newFixedThreadPool(parallel)
    )

    // Map the iterator into a stream of futures
    iterator.map(item => Future(f(item)))
  }

  def awaitAll[B](futures: Iterator[Future[B]]): Iterator[B] = {
    futures.map(Await.result(_, scala.concurrent.duration.Duration.Inf))
  }

  def main(args: Array[String]): Unit = {
    val numbers = Iterator.range(1, 1000)

    val greppedWith1337 = Processing.mapAsync(4, numbers, (x: Int) => {
      val is = new ByteArrayInputStream(x.toString.getBytes())
      val proc = os.spawn(cmd = Seq("/usr/bin/grep","1337"),stdin = is)
      val res = Source.fromInputStream(proc.stdout.wrapped).getLines().mkString("\n")
      println(proc.exitCode())
      res
    })

    val stringFutures = Processing.awaitAll(greppedWith1337).toList

    stringFutures.foreach(println)

//    // First async transformation
//    val squaredFutures = Processing.mapAsync[Int,Int](4, numbers, x => {
//      println(s"Squaring $x in thread ${Thread.currentThread().getName}")
//      x * x
//    })
//
//    // Second async transformation (chained)
//    val stringFutures = Processing.mapAsync(2, squaredFutures.map(Await.result(_, scala.concurrent.duration.Duration.Inf)), (x: Int) => {
//      println(s"Converting $x to string in thread ${Thread.currentThread().getName}")
//      x.toString
//    })
//
//    // If you need to collect all results (blocking)
//    val results = Processing.awaitAll(stringFutures).toList
//    println(s"Final Results: $results")
  }
}
