# client
The client part of the Spatial Metabolomics project

Contains a converter for file formats; converts from imzML (http://imzml.org/download/imzml/specifications_imzML1.1.0_RC1.pdf)
file format to Parquet (http://parquet.apache.org) file format.

## Installation requirements
- Java 1.6+
- Hadoop

## Run instructions 

Get the jar ipconverter-1.0.0-standalone.jar, then run it as:

``` 
hadoop jar ipconverter-1.0.0-standalone.jar <input-filename> <output-filename>

For example:

hadoop jar ipconverter-1.0.0-standalone.jar sample_data/Example_Processed sample_data/ex_out
```

Make sure that when you specipy input-filename Example_Processed, then, Example_Processed.ibd, and Example_Processed.imzML  already exist in the location. The output file with a name ex_out.parquet will be created in the folder sample_data. 
The output file should not be present at the location, only then a new file will be created.

#View output
You can view the contents of the Parquet file using the Parquet tools, as:

```
hadoop jar ./parquet-tools-<VERSION>.jar <command> my_parquet_file.parquet

For example
hadoop jar ./parquet-tools-<VERSION>.jar meta sample_data/ex_out.parquet
hadoop jar ./parquet-tools-<VERSION>.jar dump sample_data/ex_out.parquet
hadoop jar ./parquet-tools-<VERSION>.jar head sample_data/ex_out.parquet

If the file is not too large
hadoop jar ./parquet-tools-<VERSION>.jar cat sample_data/ex_out.parquet > sample_data/ex_out_cat.txt

```

#New feature to be added soon
Choice of compression for the Parquet file.





