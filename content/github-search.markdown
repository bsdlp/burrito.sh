Title: find /github -name id_rsa
Date: 2013-01-24 22:45
Author: jchen
Category: blog
Tags: random internet news, web
Slug: github-search

So, the new [GitHub code search feature][] has got people buzzing about
publicly committed ssh private keys. Then, people get [a little worked
up][] about how GitHub should add a default gitignore or something to
prevent people from committing stuff they shouldn't commit.

<!-- PELICAN_END_SUMMARY -->

Why?

GitHub already has a helpful guide for how to [remove committed
sensitive data][]. I don't believe that it is GitHub's responsibility to
make sure people aren't committing private keys or secret tokens. I do
agree with guptaneil on his later point that it might be a good idea for
GitHub to check if people committed stuff they shouldn't have committed,
such as looking for a file that begins with
`-----BEGIN RSA PRIVATE KEY-----`, then warning the user on the web app
about said commit. That probably wouldn't be terribly effective, as I
think most people use git cli instead of directly coding/committing on
github.com.

With that being said, this new code search function is awesome!

*2013-01-25 12:12 UPDATE:*
Apparently GitHub's search is [down][]? Doing a [search for
.ssh/id\_rsa][] does return empty, and I doubt that's because users
actually took down their keys. Interesting. According to the article
that Slashdot references, the search function is down due to technical
difficulties, but I wonder if GitHub may consider continuing to block
searches for private keys. Hopefully not.

  [GitHub code search feature]: https://github.com/blog/1381-a-whole-new-code-search
    "github code search"
  [a little worked up]: http://news.ycombinator.com/item?id=5105609
  [remove committed sensitive data]: https://help.github.com/articles/remove-sensitive-data
    "github remove sensitive data"
  [down]: http://it.slashdot.org/story/13/01/25/132203/github-kills-search-after-hundreds-of-private-keys-exposed
  [search for .ssh/id\_rsa]: https://github.com/search?q=path%3A.ssh%2Fid_rsa&type=Code&ref=searchresults
    "github search for .ssh/id_rsa"

