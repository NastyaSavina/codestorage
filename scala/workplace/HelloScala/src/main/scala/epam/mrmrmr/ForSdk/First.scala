import scala.io.StdIn._
import scala.util.matching.Regex

object Main {
  def main(args: Array[String]) {
    val input = "lol__kek_"

    val snakeCaseRegexWithUnderscore = "^[a-z|_]+$"
    println("SnakeCase with underscore: " + input.matches(snakeCaseRegexWithUnderscore))

    val snakeCaseRegexWithoutUnderscore = "^_.+|_$"

    println("SnakeCase without underscore: " + input.matches(snakeCaseRegexWithoutUnderscore))


    val containsUnderscore2 = ".+_{2}.+"
    println("_{2}: " + input.matches(containsUnderscore2))

  }
}
