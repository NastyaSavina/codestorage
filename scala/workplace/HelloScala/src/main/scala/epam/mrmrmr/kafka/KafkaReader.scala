package epam.mrmrmr.kafka

import org.apache.spark.sql.SparkSession

object KafkaReader {
  def main(args: Array[String]): Unit = {
    val session = SparkSession
      .builder()
      .appName("MyApp")
      .master("local[*]")
      .getOrCreate()

    val df = session
      .read
      .format("kafka")

  }
}
