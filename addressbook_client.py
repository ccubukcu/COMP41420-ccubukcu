# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import addressbook_pb2
import random

_TIMEOUT_SECONDS = 10

_PERSON_ADD_COUNT = 3

def create_person(stub):
    user_id = random.randrange(0, 10000)
    user_name_suffix = random.randrange(0, 10000)
    username = "User " + repr(user_name_suffix)
    email = repr(user_name_suffix) + "@mail.com"

    response = stub.AddPerson(addressbook_pb2.Person(name=username, id=user_id, email=email), _TIMEOUT_SECONDS)
    print "Response: " + response.message

def print_people(stub):
    address_book = stub.ListPersons(addressbook_pb2.ListPersonsRequest(), _TIMEOUT_SECONDS)
    for person in address_book.person:
        print "Person ID:", person.id
        print "  Name:", person.name
        if person.HasField('email'):
          print "  E-mail address:", person.email

        for phone_number in person.phone:
          if phone_number.type == addressbook_pb2.Person.MOBILE:
            print "  Mobile phone #: ",
          elif phone_number.type == addressbook_pb2.Person.HOME:
            print "  Home phone #: ",
          elif phone_number.type == addressbook_pb2.Person.WORK:
            print "  Work phone #: ",
          print phone_number.number

def run():
  with addressbook_pb2.early_adopter_create_PersonService_stub('localhost', 50051) as stub:

    print
    print "*********************************"
    print "Adding 3 entries the address book"
    print "*********************************"
    print

    for i in range(0, _PERSON_ADD_COUNT):
        create_person(stub)

    print
    print "***************************************"
    print "Listing all entries in the address book"
    print "***************************************"
    print
    print_people(stub)

if __name__ == '__main__':
  run()

