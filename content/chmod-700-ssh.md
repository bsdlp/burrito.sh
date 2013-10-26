Title: chmod 700 ~/.ssh
Date: 2012-03-14 15:21
Author: jchen
Category: bash, linux
Tags: ssh config permissions chmod
Slug: chmod-700-ssh

So I keep forgetting that you need the following permissions for \~/.ssh
and its contents:

    chmod 700 ~/.ssh
    chmod 644 *.pub
    chmod 600 config
    chmod 600 id_rsa

Otherwise it'll keep complaining that your permissions are wrong.
