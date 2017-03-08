#!/usr/bin/env python
#
# Copyright 2014-2017 by Akira Yoshiyama <akirayoshiyama@gmail.com>.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Block Storage API Test (Volume Types/QoS)"""


from yakumo.smoketest import *
from yakumo import utils


def main(c):

    # QoS

    LOG.info("Create QoS #1")
    name = get_random_str('qos')
    with c.volume_type_qos.create(name=name,
                                  availability="100",
                                  numberOfFailures="0") as q1:

        LOG.debug("QoS #1: %s", q1.get_attrs())
        test("QoS #1 is created", q1 is not None)
        test("QoS #1 name is " + name, q1.name == name)
        test("Metadata: availability -> 100", q1.availability == "100")
        test("Metadata: numberOfFailures -> 0", q1.numberOfFailures == "0")

        q1.set_metadata(foo="bar", foo2="bar2")
        LOG.debug("QoS #1: %s", q1.get_attrs())
        test("Metadata: availability -> 100", q1.availability == "100")
        test("Metadata: numberOfFailures -> 0", q1.numberOfFailures == "0")
        test("Metadata: foo -> 'bar'", q1.foo == "bar")
        test("Metadata: foo2 -> 'bar2'", q1.foo2 == "bar2")

        q1.unset_metadata('availability', 'numberOfFailures')
        LOG.debug("QoS #1: %s", q1.get_attrs())
        test("Metadata: availability is None", q1.availability is None)
        test("Metadata: numberOfFailures is None", q1.numberOfFailures is None)
        test("Metadata: foo -> 'bar'", q1.foo == "bar")
        test("Metadata: foo2 -> 'bar2'", q1.foo2 == "bar2")

        LOG.info("Create Volume Type #1")
        name = get_random_str('volume')
        with c.volume_type.create(name=name,
                                  description='volume type 1',
                                  is_public=False) as vt1:

            test("Volume Type #1 is created", vt1 is not None)
            test("Volume Type #1 name is " + name, vt1.name == name)

            LOG.info("Create Volume Type #2")
            name = get_random_str('volume')
            with c.volume_type.create(name=name,
                                      description='volume type 2',
                                      is_public=False) as vt2:

                test("Volume Type #2 is created", vt2 is not None)
                test("Volume Type #2 name is " + name, vt2.name == name)

                LOG.debug("Volume Type #1: associate with QoS #1")
                q1.associate(vt1)
                a1 = q1.get_associations()
                LOG.debug("QoS #1 associations: %s", a1)
                test("Volume Type #1: associated with QoS #1", vt1 in a1)

                LOG.debug("Volume Type #2: associate with QoS #1")
                q1.associate(vt2)
                a1 = q1.get_associations()
                LOG.debug("QoS #1 associations: %s", a1)
                test("Volume Type #2: associated with QoS #1", vt2 in a1)

                LOG.debug("Volume Type #1: disassociate from QoS #1")
                q1.disassociate(vt1)
                a1 = q1.get_associations()
                LOG.debug("QoS #1 associations: %s", a1)
                test("Volume Type #1: not associated with QoS #1",
                     vt1 not in a1)

                LOG.debug("Volume Type #2: disassociate from QoS #1")
                q1.disassociate(vt2)
                a1 = q1.get_associations()
                LOG.debug("QoS #1 associations: %s", a1)
                test("Volume Type #2: not associated with QoS #1",
                     vt2 not in a1)

                LOG.debug("Volume Type #1, #2: associate with QoS #1")
                q1.associate(vt1, vt2)
                a1 = q1.get_associations()
                LOG.debug("QoS #1 associations: %s", a1)
                test("Volume Type #1: associated with QoS #1", vt1 in a1)
                test("Volume Type #2: associated with QoS #1", vt2 in a1)

                LOG.debug("All Volume Type: disassociate from QoS #1")
                q1.disassociate_all()
                a1 = q1.get_associations()
                LOG.debug("QoS #1 associations: %s", a1)
                test("No volume type associated with QoS #1", a1 == [])

            test("Volume Type #2 is deleted", vt1 not in c.volume.list())

        test("Volume Type #1 is deleted", vt1 not in c.volume.list())

    test("QoS #1 is deleted", q1 not in c.volume.list())


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list volume types: %s", [_.name for _ in c.volume_type.list()])
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list QoS: %s", [_.name for _ in c.volume_type_qos.list()])
    main(c)
    LOG.debug("list volume types: %s", [_.name for _ in c.volume_type.list()])
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list QoS: %s", [_.name for _ in c.volume_type_qos.list()])

    show_test_summary()
