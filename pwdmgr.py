#!/usr/bin/env python3
import json
import os
import argparse

class pwdDB(object):
  def __init__(self , location='pwd.json'):
    self.location = os.path.expanduser(location)
    self.load(self.location)

  def load(self , location):
    if os.path.exists(location):
      self._load()
    else:
      self.db = {}
    return True

  def _load(self):
    self.db = json.load(open(self.location , "r"))

  def dumpdb(self):
    try:
      json.dump(self.db , open(self.location, "w+"))
      return True
    except:
      return False

  def set(self, args):
    try:
      self.db[str(args.key)] = args.value
      self.dumpdb()
      return True
    except Exception as e:
      print("[X] Error Saving Values to Database : " + str(e))
      return False

  def get(self, args):
    try:
      return self.db[args.key]
    except KeyError:
      print("No Value Can Be Found for " + str(args.key))  
      return False

  def delete(self, args):
    if not args.key in self.db:
      return False
    del self.db[args.key]
    self.dumpdb()
    return True

def parse_args(pwdDB):
  parser = argparse.ArgumentParser()
  parser.set_defaults(func=lambda _: parser.print_usage())
  subparsers = parser.add_subparsers()

  parser_get = subparsers.add_parser('get')
  parser_get.add_argument('-key')
  parser_get.set_defaults(func=pwdDB.get)

  parser_put = subparsers.add_parser('set')
  parser_put.add_argument('-key')
  parser_put.add_argument('-value')
  parser_put.set_defaults(func=pwdDB.set)
  parser.parse_args()
  return parser.parse_args()

if __name__ == "__main__":
  pwddb = pwdDB()
  args = parse_args(pwddb)
  result = args.func(args)
  if result:
    print(result)