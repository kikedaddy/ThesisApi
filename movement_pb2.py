# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: movement.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='movement.proto',
  package='whatever',
  serialized_pb=_b('\n\x0emovement.proto\x12\x08whatever\"*\n\x04Move\x12\x10\n\x08steering\x18\x02 \x01(\x02\x12\x10\n\x08movement\x18\x03 \x01(\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_MOVE = _descriptor.Descriptor(
  name='Move',
  full_name='whatever.Move',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='steering', full_name='whatever.Move.steering', index=0,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='movement', full_name='whatever.Move.movement', index=1,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=70,
)

DESCRIPTOR.message_types_by_name['Move'] = _MOVE

Move = _reflection.GeneratedProtocolMessageType('Move', (_message.Message,), dict(
  DESCRIPTOR = _MOVE,
  __module__ = 'movement_pb2'
  # @@protoc_insertion_point(class_scope:whatever.Move)
  ))
_sym_db.RegisterMessage(Move)


# @@protoc_insertion_point(module_scope)