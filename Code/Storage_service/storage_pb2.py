# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: storage.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rstorage.proto\x12\x07storage\"\r\n\x0b\x44\x61taRequest\"+\n\x0c\x44\x61taResponse\x12\r\n\x05\x66ound\x18\x01 \x01(\x08\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"\"\n\x12\x44\x61taStorageRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"&\n\x13\x44\x61taStorageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x90\x01\n\x0eStorageService\x12\x36\n\x07GetData\x12\x14.storage.DataRequest\x1a\x15.storage.DataResponse\x12\x46\n\tStoreData\x12\x1b.storage.DataStorageRequest\x1a\x1c.storage.DataStorageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'storage_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DATAREQUEST']._serialized_start=26
  _globals['_DATAREQUEST']._serialized_end=39
  _globals['_DATARESPONSE']._serialized_start=41
  _globals['_DATARESPONSE']._serialized_end=84
  _globals['_DATASTORAGEREQUEST']._serialized_start=86
  _globals['_DATASTORAGEREQUEST']._serialized_end=120
  _globals['_DATASTORAGERESPONSE']._serialized_start=122
  _globals['_DATASTORAGERESPONSE']._serialized_end=160
  _globals['_STORAGESERVICE']._serialized_start=163
  _globals['_STORAGESERVICE']._serialized_end=307
# @@protoc_insertion_point(module_scope)