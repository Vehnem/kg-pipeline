package ai.scads.kg.core.driver

import scala.collection.mutable

object IteratorSplitter {
  def split[A](iterator: Iterator[A], numIterators: Int): Seq[Iterator[A]] = {
    require(numIterators > 0, "Number of iterators must be greater than 0")

    val queues: Array[mutable.Queue[A]] = Array.fill(numIterators)(mutable.Queue[A]())

    @volatile var itemCount = 0

    def distributeNext(): Unit = synchronized {
      if (iterator.hasNext) {
        val item = iterator.next()
        val targetIndex = itemCount % numIterators
        queues(targetIndex).enqueue(item)
        itemCount += 1
      }
    }

    val iterators: Seq[Iterator[A]] = queues.zipWithIndex.map { case (queue, index) =>
      new Iterator[A] {
        override def hasNext: Boolean = queue.nonEmpty || iterator.hasNext
        override def next(): A = synchronized {
          while (queue.isEmpty && iterator.hasNext) {
            distributeNext()
          }
          if (queue.nonEmpty) queue.dequeue()
          else throw new NoSuchElementException("No more elements")
        }
      }
    }

    iterators
  }
}


object IteratorSplitterMain extends App {
  val original = Iterator.range(1, 10) // Example: 1 to 9
  val splitIterators = IteratorSplitter.split(original, 3)

  // Each thread can process one iterator independently
  splitIterators.zipWithIndex.foreach { case (it, idx) =>
    println(s"Iterator $idx: " + it.toList.mkString(", "))
  }
}
