#!/usr/bin/env python2.7
## protoc -I/usr/local/include/ -I. --python_out=. format.proto
# protoc -I/usr/local/Cellar/protobuf/3.6.1.3_1/include/ -I. --python_out=. format.proto

# to run:

# python -m pdb ./test_danbooru.py <(jq '' format.txt -c -M)

import os, sys, json
from pprint import pprint

import protobuf_json

import format_pb2 as db_test
from google.protobuf import timestamp_pb2


"""
# create and fill test message
pb=db_test.Entry()
pb.id=123
pb.b=b"\x08\xc8\x03\x12"
pb.query="some text"
pb.flag=True
pb.test_enum=2
msg=pb.nested_msg
msg.id=1010
msg.title="test title"
msg.url="http://example.com/"

msgs=pb.nested_msgs.add()
msgs.id=456
msgs.title="test title"
msgs.url="http://localhost/"

pb.rep_int.append(1)
pb.rep_int.append(2)

pb.bs.append("\x00\x01\x02\x03\x04");
pb.bs.append("\x05\x06\x07\x08\x09");

# convert it to JSON and back
pprint(pb.SerializeToString())
json_obj=protobuf_json.pb2json(pb)
"""

from dateutil.parser import parse

def parsetime(x):
  dt = parse(x)
  if dt.utcoffset() is not None:
    return dt.replace(tzinfo=None) - dt.utcoffset()
  else:
    return dt.replace(tzinfo=None)

args = sys.argv[1:]

def get_input():
  if len(args) > 0:
    for arg in args:
      with open(arg) as f:
        for line in f:
          yield line
  else:
    for line in sys.stdin:
      yield line
#with open('format.txt') as f:
  #json_obj = json.load(f)
import datetime
for line in get_input():
  try:
    json_obj = json.loads(line)
    for k in json_obj.keys():
      if k.endswith('_at'):
        v = json_obj[k]
        #if '.' in v:
        #  dt = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S.%f UTC')
        #else:
        #  dt = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S UTC')
        #if not '.' in v:
        #  v = v.replace(' UTC', '.000 UTC')
        #v = v.replace(' UTC', 'Z').replace(' ', 'T')
        #v = parse(v).utcnow().isoformat() + 'Z'
        #ts = timestamp_pb2.Timestamp()
        #ts.FromJsonString(v)
        #v = ts.ToJsonString()
        v = parsetime(v).isoformat() + 'Z'
        json_obj[k] = v
  except:
    import traceback
    traceback.print_exc()
    continue
  #pprint(json_obj)
  pb2=protobuf_json.json2pb(db_test.Entry(), json_obj)
  raw = pb2.SerializeToString()
  json_obj2 = protobuf_json.pb2json(pb2)
  pprint(json_obj2)
import pdb
pdb.set_trace()

#if pb == pb2:
#	print("Test passed.")
#else:
#	print("Test FAILED!")
