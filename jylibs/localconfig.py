#
# SPDX-FileCopyrightText: 2021 Synacor, Inc.
#
# SPDX-License-Identifier: GPL-2.0-only
#


import time

import commands
import config
from logmsg import *


class LocalConfig(config.Config):
  def load(self):
    self.loaded = True

    t1 = time.clock()
    c = commands.commands["localconfig"]
    rc = c.execute();
    if (rc != 0):
      Log.logMsg(1, "Skipping "+c.desc+" update.");
      Log.logMsg(1, str(c));
      return None
    dt = time.clock()-t1
    Log.logMsg(5,"Localconfig fetched in %.2f seconds (%d entries)" % (dt,len(c.output)))

    if (len(c.output) == 0):
      Log.logMsg(2, "Skipping " + c.desc + " No data returned.")
      c.status = 1
      raise Exception("Skipping " + c.desc + " No data returned.")

    self.config = dict([(k,v) for (k,v) in c.output])

    # Set a default for this
    if self["zmconfigd_listen_port"] is None:
      self["zmconfigd_listen_port"] = "7171"

    if self["ldap_url"] is not None:
      v = self["ldap_url"]
      v = str(v)
      self["opendkim_signingtable_uri"] = ' '.join([''.join((val,'/?DKIMSelector?sub?(DKIMIdentity=$d)')) for val in self["ldap_url"].split()])
      self["opendkim_keytable_uri"] = ' '.join([''.join((val,'/?DKIMDomain,DKIMSelector,DKIMKey,?sub?(DKIMSelector=$d)')) for val in self["ldap_url"].split()])

    dt = time.clock()-t1
    Log.logMsg(5,"Localconfig loaded in %.2f seconds" % dt)
