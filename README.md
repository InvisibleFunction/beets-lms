# beets-lms

This is a plugin for integrating Lyrion Music Server (LMS) with Beets.

Currently it implements a listener to trigger a library rescan on import. You can also manually trigger a rescan or check the rescan status.

## Installation
`pip`:

```
pip install git+https://github.com/InvisibleFunction/beets-lms
```

## Configuration

Add `beets-lms` to your list of plugins in your configfile:

```
plugins: beets-lms
```

Configure the hostname or ip address for your LMS server:

```
beets_lms:
  host: 192.168.255.16
```

## Functionality

* `import` listener to trigger rescan on import
* `lmsstatus` subcommand to check scanning status
* `lmsrescan` subcommand to manually trigger rescan

```
me@compy:~$ beet lmsstatus
beets-lms: LMS not currently scanning
me@compy:~$ beet lmsrescan
beets-lms: LMS library rescan triggered.
me@compy:~$ beet lmsstatus
beets-lms: LMS Library scan in progress
```


