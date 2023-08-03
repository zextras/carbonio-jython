#
# SPDX-FileCopyrightText: 2021 Synacor, Inc.
#
# SPDX-License-Identifier: GPL-2.0-only
#


from logmsg import *
import commands
import config
import re
import time

class GlobalConfig(config.Config):
	def load(self):
		self.loaded = True

		t1 = time.clock()
		c = commands.commands["gacf"]
		rc = c.execute();
		if (rc != 0):
			Log.logMsg(1, "Skipping "+c.desc+" update.");
			Log.logMsg(1, str(c));
			return None

		# if no output was returned we have a potential avoid stopping all services
		if (len(c.output) == 0):
			Log.logMsg(2, "Skipping " + c.desc + " No data returned.")
			c.status = 1
			return None

		self.config = dict([(e.getKey(), e.getValue()) for e in sorted(c.output, key=lambda x: x.getKey())])

		if self["zimbraMtaBlockedExtensionWarnRecipient"] == "TRUE" and self["zimbraAmavisQuarantineAccount"] is not None:
			self["zimbraQuarantineBannedItems"] = 'TRUE'
		else:
			self["zimbraQuarantineBannedItems"] = 'FALSE'

		if self["zimbraMailboxdSSLProtocols"] is not None:
			v = self["zimbraMailboxdSSLProtocols"]
			v = str(v)
			self["zimbraMailboxdSSLProtocols"] = ' '.join(sorted(v.split(), key=str.lower))
			self["zimbraMailboxdSSLProtocolsXML"] = '\n'.join([''.join(('<Item>',val,'</Item>')) for val in self["zimbraMailboxdSSLProtocols"].split()])

		if self["zimbraSSLExcludeCipherSuites"] is not None:
			v = self["zimbraSSLExcludeCipherSuites"]
			v = str(v)
			self["zimbraSSLExcludeCipherSuites"] = ' '.join(sorted(v.split(), key=str.lower))
			self["zimbraSSLExcludeCipherSuitesXML"] = '\n'.join([''.join(('<Item>',val,'</Item>')) for val in self["zimbraSSLExcludeCipherSuites"].split()])

		if self["zimbraSSLIncludeCipherSuites"] is not None:
			v = self["zimbraSSLIncludeCipherSuites"]
			v = str(v)
			self["zimbraSSLIncludeCipherSuites"] = ' '.join(sorted(v.split(), key=str.lower))
			self["zimbraSSLIncludeCipherSuitesXML"] = '\n'.join([''.join(('<Item>',val,'</Item>')) for val in self["zimbraSSLIncludeCipherSuites"].split()])

		dt = time.clock()-t1
		Log.logMsg(5,"globalconfig loaded in %.2f seconds" % dt)
