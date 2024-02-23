mkdir -p tools

cd tools
rm -rf rmlmapper-java
git clone git@github.com:RMLio/rmlmapper-java.git
cd rmlmapper-java
mvn clean package -DskipTests -P no-buildnumber
cp target/rmlmapper-*-all.jar ../rmlmapper.jar