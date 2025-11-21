#
# SPDX-FileCopyrightText: 2021 Synacor, Inc.
#
# SPDX-License-Identifier: GPL-2.0-only
#

import os
import re

from org.graylog2.syslog4j import Syslog
from org.graylog2.syslog4j import SyslogConstants
from org.graylog2.syslog4j.impl.unix.socket import UnixSocketSyslogConfig

import conf


class Log:
	zmconfigdSyslogInstance = UnixSocketSyslogConfig(SyslogConstants.FACILITY_LOCAL0, "/dev/log")
	zmsyslog = Syslog.createInstance("zmSyslog",zmconfigdSyslogInstance)
	zmsyslog.getConfig().setLocalName("zmconfigd[%d]:" % os.getpid())

	@classmethod
	def initLogging(cls, c = None):
		if c:
			cls.cf = c
			if cls.cf.loglevel > 5:
				cls.cf.loglevel = 5
		else:
			cls.cf = conf.Config()

	@classmethod
	def logMsg(cls, lvl, msg):

		if lvl > 5:
			lvl = 5
		msg = re.sub(r"\s|\n", " ", msg)

		if lvl <= cls.cf.loglevel:
			Log.zmsyslog.log(lvl, msg)

		if lvl == 0:
			Log.zmsyslog.log(2, "%s: shutting down" % (cls.cf.progname,) )
			os._exit(1)

Log.initLogging()
