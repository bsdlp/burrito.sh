Title: cffunction context validation error
Date: 2014-05-10 15:29
Author: jchen
Category: blog
Tags: linux
Slug: cffunction-context-error

[![cffunction context validation error](/thumbs/cffunction_context_validation_thumbnail_wide.png)](/img/cffunction_context_validation.png)

So you're hacking on some coldfusion.

> Context validation error for the cffunction tag.
> 
> The start tag must have a matching end tag. An explicit end tag can be provided
> by adding `</cffunction>`. If the body of the tag is empty, you can use the
> shortcut `<cffunction …/>`.

If you have your `<cffunction>` tag somewhere to start your function, and then
some `<cfarguments>` jawns to define function variables, and you've made sure
that you've got a closing `</cffunction>` tag, then you've probably got
something in between your `<cffunction>` tag and your `<cfarguments>` tags.

Woohoo non-obvious errors.
