# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: internal.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import proto.kgs.gateway.v1.server_pb2 as server__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0einternal.proto\x12\x0ekgs.gateway.v1\x1a\x0cserver.proto\"7\n\x1a\x43loseUserConnectionRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\"-\n\x1b\x43loseUserConnectionResponse\x12\x0e\n\x06result\x18\x01 \x01(\r2\xf3\x05\n\x0eGatewayService\x12\x64\n\x0f\x46orwardToClient\x12&.kgs.gateway.v1.ForwardToClientRequest\x1a\'.kgs.gateway.v1.ForwardToClientResponse\"\x00\x12s\n\x14\x42\x61tchForwardToClient\x12+.kgs.gateway.v1.BatchForwardToClientRequest\x1a,.kgs.gateway.v1.BatchForwardToClientResponse\"\x00\x12\x61\n\x0eSetUserService\x12%.kgs.gateway.v1.SetUserServiceRequest\x1a&.kgs.gateway.v1.SetUserServiceResponse\"\x00\x12k\n\x16VerifyUserOnlineStatus\x12&.kgs.gateway.v1.QueryUserStatusRequest\x1a\'.kgs.gateway.v1.QueryUserStatusResponse\"\x00\x12m\n\x12SetUserIdleTimeout\x12).kgs.gateway.v1.SetUserIdleTimeoutRequest\x1a*.kgs.gateway.v1.SetUserIdleTimeoutResponse\"\x00\x12p\n\x13\x43loseUserConnection\x12*.kgs.gateway.v1.CloseUserConnectionRequest\x1a+.kgs.gateway.v1.CloseUserConnectionResponse\"\x00\x12U\n\nCallClient\x12!.kgs.gateway.v1.CallClientRequest\x1a\".kgs.gateway.v1.CallClientResponse\"\x00\x42x\n\"com.kingsoft.shiyou.kgs.gateway.v1B\rInternalProtoP\x01ZAgit.shiyou.kingsoft.com/server/kgs-apis/go/kgs/gateway/v1;gatewayb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'internal_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.kingsoft.shiyou.kgs.gateway.v1B\rInternalProtoP\001ZAgit.shiyou.kingsoft.com/server/kgs-apis/go/kgs/gateway/v1;gateway'
  _CLOSEUSERCONNECTIONREQUEST._serialized_start=48
  _CLOSEUSERCONNECTIONREQUEST._serialized_end=103
  _CLOSEUSERCONNECTIONRESPONSE._serialized_start=105
  _CLOSEUSERCONNECTIONRESPONSE._serialized_end=150
  _GATEWAYSERVICE._serialized_start=153
  _GATEWAYSERVICE._serialized_end=908
# @@protoc_insertion_point(module_scope)