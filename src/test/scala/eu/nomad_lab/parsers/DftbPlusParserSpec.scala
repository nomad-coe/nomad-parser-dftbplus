package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object DftbPlusTests extends Specification {
  "DftbPlusParserTest" >> {
    "test with json-events" >> {
      ParserRun.parse(DftbPlusParser, "parsers/dftbPlus/test/examples/detailed.out", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json" >> {
      ParserRun.parse(DftbPlusParser, "parsers/dftbPlus/test/examples/detailed.out", "json") must_== ParseResult.ParseSuccess
    }
  }
}
