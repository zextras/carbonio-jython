#
# SPDX-FileCopyrightText: 2021 Synacor, Inc.
#
# SPDX-License-Identifier: GPL-2.0-only
#


from logmsg import *
import commands
import config
import re
import threading
import time

class MiscConfig(config.Config):
	def load(self):
		self.loaded = True

		t1 = time.clock()
		#th = []
		for cm in commands.miscCommands:
			self.doCommand(cm);
			#th.append(threading.Thread(target=MiscConfig.doCommand,args=(self,cm),name=cm))
		
		#[t.setDaemon(True) for t in th]
		#[t.start() for t in th]
		#[t.join(60) for t in th]
		dt = time.clock()-t1
		Log.logMsg(5,"Miscconfig loaded in %.2f seconds" % dt)


	def doCommand(self, cm):
		c = commands.commands[cm]
		rc = c.execute();
		if (rc != 0):
			Log.logMsg(1, "Skipping "+c.desc+" update.");
			Log.logMsg(1, str(c));
			return None

		# lines = c.output.splitlines()

		# if no output was returned we have a potential avoid stopping all services
		if (len(c.output) == 0):
			Log.logMsg(2, "Skipping " + c.desc + " No data returned.")
			c.status = 1
			return

		self[c.name] = ' '.join(c.output)
		Log.logMsg(5, "%s=%s" % (c.name, self[c.name]));
		# v = ' '.join(lines)
		# self[cm] = self[cm] and (self[cm] + " " + v) or v

