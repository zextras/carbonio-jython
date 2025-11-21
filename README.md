# carbonio-jython

![Contributors](https://img.shields.io/github/contributors/zextras/carbonio-jython "Contributors")
![Activity](https://img.shields.io/github/commit-activity/m/zextras/carbonio-jython "Activity") ![License](https://img.shields.io/badge/license-GPL%202-green
"License")
![Project](https://img.shields.io/badge/project-carbonio-informational
"Project")
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/zextras.svg?style=social&label=Follow%20%40zextras)](https://twitter.com/zextras)

## Architecture
Example:
`zmmtactl -> configrewrite -> write to socket -> zmconfigd reads it -> 
executes actions`

Other examples:
- antivirusctl -> calls configrewrite -> writes to socket
- amavisdctl
- opendkimctl
- saslauthdctl
- clamdctl
- mtactl
- postfix

When zmconfigd receives a command, it executes the section written in 
configd.cf file.  

For example the command `configrewrite mailbox opendkim` it executes the 
commands in the section of configd. When dependencies are encountered it 
runs also those.




```
## License

See [COPYING](COPYING) file for details
