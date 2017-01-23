This repository is an excercise in prototyping possible alternatives to the
traditional jUnit XML output that is currently used by most test frameworks.
The desired outcome is a test result format that is easier to parse and is
easier to consume by document data stores. This would make test result data
much easier to use with existing tools such as Splunk and Elasticsearch.

This repository contains three executables:

junitxml2jresult
----------------

This utility will take a file or piped-in stream of junit XML content and
convert it to a jresult file.

validate-jresult
----------------

This utility will take a file or piped-in stream of content and verify if the
content matches the jresult schema. This is performed using Python's
jsonschema library. The actual schema is defined in the jresult.jresult_schema
package.

jresult2splunk
--------------

This script will take a jresult file or stream, normalize the single result
into a series of individual result objects, and insert those results into a
Splunk instance. This normalized format contains the same information as
the jresult data, but treats each test result as its own document. This may
be the ideal format for this data, so the intermediate jresult format may
end up not being necessary.