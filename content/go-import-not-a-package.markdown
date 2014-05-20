Title: Not a package file
Date: 2014-05-19 10:40
Author: jchen
Category: blog
Tags: errors, golang, dev
Slug: golang-not-a-package-file

[![error](/thumbs/golang-package-import_thumbnail_wide.jpg)](https://flic.kr/p/5w2XFL)

<!-- PELICAN_BEGIN_SUMMARY -->
So you're screwing around with your golang installation, and you've screwed up
your `GOPATH`/`GOROOT` at some point. You've figured out that `GOPATH` is in your
homedir or somesuch, and `GOROOT` is `/usr/local/whateverthehell`. So everything
works, right?

```shell
> go get github.com/kisielk/gotool
import /root/go/pkg/linux_amd64/github.com/kisielk/gotool.a: not a package file
```
<!-- PELICAN_END_SUMMARY -->

Just `rm -rf $GOPATH/pkg`, and magically everything is fixed.

Woohoo non-obvious errors.
