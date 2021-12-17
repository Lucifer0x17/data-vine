import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


def json_to_avro(delta, avro_filepath, avsc_filepath):
    schema = avro.schema.parse(open(avsc_filepath).read())
    writer = DataFileWriter(open(avro_filepath, "wb"),
                            DatumWriter(), schema, codec='deflate')
    for record in delta:
        writer.append(record)
    writer.close()


def avro_to_json(avro_filepath):
    with open(avro_filepath, "rb") as f:
        reader = DataFileReader(f, DatumReader())
        users = [user for user in reader]
        reader.close()
    return users
