package epam.mrmrmr.ForSdk

import java.io.{ByteArrayInputStream, FileInputStream}

import scala.io.{BufferedSource, Source}

object PersonReader {
  def read(): Seq[Person] = {
    val inputStream = new FileInputStream("/Users/me/data.csv");
    val source: BufferedSource = Source.fromInputStream(inputStream)
    val lines = source.getLines()
    val persons: Iterator[Person] = lines.map(line => {
          val parts: Array[String] = line.split(",")
          Person(parts(0), parts(1), parts(2).toInt, parts(3))
        })

    persons.toSeq
  }
}

object PersonPrinter {
  def main(args: Array[String]): Unit = {
    val persons = PersonReader.read()
    persons.foreach(println)

//    val df = spark.


  }
}

case class Person (name: String, surname: String, age: Int, position: String)