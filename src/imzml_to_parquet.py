# -*- coding: UTF-8 -*-

# Spatial Metabolomics
#
# Copyright 2015 EMBL
# @author Shefali Sharma, Dominik Fay
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Converter for files in the imzML file format (http://imzml.org/download/imzml/specifications_imzML1.1.0_RC1.pdf)
to a Parquet (http://parquet.apache.org) file format. It acceses the pyImzML parser to extract
each spectrum from the .ibd file.

Uses Jython to access Parquet's Java API. A combined .jar with the Jython libraries, the Python code, 
and dependent jars is available for download. Run the jar with:

hadoop jar ipconverter-1.0.0-standalone.jar <input-filename> <output-filename>

"""

import sys
from pyimzml.ImzMLParser import ImzMLParser
from parquet.avro import AvroParquetWriter
from org.apache.avro import Schema
from org.apache.avro.generic import GenericRecordBuilder
from org.apache.hadoop.fs import Path

def doInsert(p, writer, schema):
    #Create a generic record
    builder = GenericRecordBuilder(schema)
    
    for i, (x,y) in enumerate(p.coordinates):
	#Get mzArray, and intensityArray
        mzA, intA = p.getspectrum(i)
        for mzV, intV in zip(mzA, intA):
	    #Set Coordinates x,y and index i
	    builder.set("x", x)
	    builder.set("y", y)
	    builder.set("i", i)
	    #Set mz and intensity values
            builder.set("mz", mzV)
	    builder.set("intensity", intV)
	    record = builder.build()
	    #Write to the Parquet file
	    writer.write(record)
        


if __name__ == "__main__":
    #Get the input filename from the command line
    inFilename = sys.argv[1] + ".imzML"
    p = ImzMLParser(inFilename)
    #Get the output filename from the command line
    parquetFilename = sys.argv[2] + ".parquet"
   
    #Describe the Avro schema 
    schema_string = """{
    "type": "record",
    "name": "Spectra",
    "fields": [
    {"name": "x", "type": "int"},
    {"name": "y", "type": "int"},
    {"name": "i", "type": "int"},
    {"name": "mz", "type": ["null", "double"]},
    {"name": "intensity", "type": ["null", "double"]}
    ]
    }"""
    
    schema = Schema.parse(schema_string)
    path = Path(parquetFilename)
    #Create a writer and passass it the Avro schema, compression and other options
    writer = AvroParquetWriter(path, schema)
        
    try:
        doInsert(p, writer, schema)
    except Exception, e:
        print(e)
    finally:
        writer.close()
