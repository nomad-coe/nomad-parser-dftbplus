package eu.nomad_lab.parsers

import eu.nomad_lab
import eu.nomad_lab.DefaultPythonInterpreter
import org.{ json4s => jn }
import eu.{ nomad_lab => lab }
import scala.collection.breakOut

object DftbPlusParser extends SimpleExternalParserGenerator(
  name = "DftbPlusParser",
  parserInfo = jn.JObject(
    ("name" -> jn.JString("DftbPlus")) ::
      ("parserId" -> jn.JString("DftbPlus" + lab.DftbPlusVersionInfo.version)) ::
      ("versionInfo" -> jn.JObject(
        ("nomadCoreVersion" -> jn.JObject(lab.NomadCoreVersionInfo.toMap.map {
          case (k, v) => k -> jn.JString(v.toString)
        }(breakOut): List[(String, jn.JString)])) ::
          (lab.DftbPlusVersionInfo.toMap.map {
            case (key, value) =>
              (key -> jn.JString(value.toString))
          }(breakOut): List[(String, jn.JString)])
      )) :: Nil
  ),
  mainFileTypes = Seq("text/.*"),
  mainFileRe = """ Fermi distribution function

""".r,
  cmd = Seq(DefaultPythonInterpreter.pythonExe(), "${envDir}/parsers/dftb-plus/parser/parser-dftb-plus/dftb-plus_parser.py",
    "--uri", "${mainFileUri}", "${mainFilePath}"),
  resList = Seq(
    "parser-dftb+/parser_dftb+.py",
    "parser-dftb+/setup_paths.py",
    "nomad_meta_info/public.nomadmetainfo.json",
    "nomad_meta_info/common.nomadmetainfo.json",
    "nomad_meta_info/meta_types.nomadmetainfo.json",
    "nomad_meta_info/dftb_plus.nomadmetainfo.json"
  ) ++ DefaultPythonInterpreter.commonFiles(),
  dirMap = Map(
    "parser-dftb-plus" -> "parsers/dftb-plus/parser/parser-dftb-plus",
    "nomad_meta_info" -> "nomad-meta-info/meta_info/nomad_meta_info",
    "python" -> "python-common/common/python/nomadcore"
  ) ++ DefaultPythonInterpreter.commonDirMapping(),
  metaInfoEnv = Some(lab.meta.KnownMetaInfoEnvs.dftbPlus)
)
