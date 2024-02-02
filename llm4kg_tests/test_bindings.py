import subprocess
import os

limes_jar="/home/marvin/src/LIMES/limes-core/target/limes-core-1.7.9.jar"
limes_config="/home/marvin/src/kg-pipeline/llm4kg_benchmark/experiments/example_bench/limes_conig2.xml"
examples_dir="/home/marvin/src/kg-pipeline/llm4kg_benchmark/experiments/example_bench"

def get_java_executable():
    return os.environ['JAVA_HOME']+'/bin/java'

def test_java_executable():
    print(get_java_executable())

def test_limes():
    print(str.join(" ",[get_java_executable(), "-jar", limes_jar, limes_config]))
    subprocess.run([get_java_executable(), "-jar", limes_jar, limes_config])

def test_java_binding():
    # Logic to execute JAVA binding
    print("Executing JAVA binding...")
