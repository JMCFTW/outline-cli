![Run tests](https://github.com/JMCFTW/outline-cli/workflows/Run%20tests/badge.svg?branch=main)
![Publish to Pypi](https://github.com/JMCFTW/outline-cli/workflows/Publish%20to%20Pypi/badge.svg)
![Code Quality Score](https://www.code-inspector.com/project/16211/score/svg)
![Code Grade](https://www.code-inspector.com/project/16211/status/svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/outline-cli)

# outline-cli
A command line tool that can help you manage your Outline VPN server more easily.
It support all the API in [this.](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/shadowbox/server/api.yml)

And more:
1. Create access key by email.
2. Batch create access key by email list.

and it will send VPN information to the user(s) by Gmail.

# How to use?
1.
```
pip install outline-cli
```

2. Put your gmail and Outline VPN credential information to app.ini.

	[Example](https://github.com/JMCFTW/outline-cli/blob/main/example-app.ini)


3. Run outline cli with following command:
```
outline-cli
```
