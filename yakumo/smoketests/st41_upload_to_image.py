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
"""Block Storage API Test (Upload volumes to Glance)"""


from yakumo.smoketest import *
from yakumo import utils


IMAGE_NAME = 'cirros'


def main(c, image=None):

    LOG.debug("image: %s", image)

    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list image: %s", [_.name for _ in c.image.list()])

    LOG.info("Create Volume #1")
    name = get_random_str('volume')
    with c.volume.create(name=name,
                         description="volume 1",
                         source=image,
                         size=1) as v1:

        test("Volume #1 is created", v1 is not None)

        LOG.debug("wait for created")
        v1.wait_for_finished()

        test("Volume #1 name is " + name, v1.name == name)
        test("Volume #1 is available", v1.status == 'available')
        test("Volume #1 source is the image", v1.source_image == image)

        LOG.info("Create Image #1 from Volume #1")
        name = get_random_str('image')
        with v1.upload(name=name, disk_format="raw") as i:

            LOG.debug("list image: %s", [_.name for _ in c.image.list()])

            test("Image #1 is created", i is not None)

            LOG.debug("wait for created")
            i.wait_for_finished()

            LOG.debug("image status: %s", i.status)
            test("Image #1 name is " + name, i.name == name)
            test("Image #1 is active", i.status == 'active')

            LOG.info("Create Volume #2 from Image #1")
            name = get_random_str('volume')
            with c.volume.create(name=name,
                                 description="volume 2",
                                 source=i,
                                 size=1) as v2:

                test("Volume #2 is created", v2 is not None)

                LOG.debug("wait for created")
                v2.wait_for_finished()

                test("Volume #2 name is " + name, v2.name == name)
                test("Volume #2 is available", v2.status == 'available')
                test("Volume #2 source is Image #1", v2.source_image == i)

            test("Volume #2 is deleted", v2 not in c.volume.list())

        test("Image #1 is deleted", i not in c.image.list())

    test("Volume #1 is deleted", v1 not in c.volume.list())

    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list image: %s", [_.name for _ in c.image.list()])

    show_test_summary()


if __name__ == '__main__':
    c = utils.get_client()
    i = c.image.find_one(name=IMAGE_NAME)
    main(c, image=i)
