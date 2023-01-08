---
name: Bug report
about: Create a minimal reproducible example to help us improve
labels: ["bug"]

---

# Provide a minimally reproducible example

To maximize the chances of your issue being fixed, you should share a minimally reproducible example that allows us to reproduce your error.  A good way to do this is to setup a new nbdev project which containts the minimal amount of code that reproduces your error.  

If we are not able to reproduce your error, we may close your issue.

## Some background on minimal reproducible examples [^1]

The first benefit of a public reproduction is to prove that the problem is not caused by your environment or by a setting you left out of your description, thinking it wasn't relevant. If there were any doubts about whether you'd found a genuine problem before, they are usually removed once a reproduction is made.

Next, when a reproduction has minimal config and code, it can often let us narrow down or even identify the root cause, suggest workarounds, etc. This means we can often help you from code inspection alone.

Finally, by making the code/dependencies minimal, it usually makes the problem feasible to step through using a debugging if code inspection wasn't sufficient. Production repositories or non-minimal reproductions are often very difficult to debug because break points get triggered dozens or hundreds or times.

The basic idea of a minimal reproduction is to use the least amount of both code and config to trigger missing or wrong behavior. A minimal reproduction helps the developers see where the bug or missing feature is, and allows us to verify that the new code meets the requirements.

## Where to host your mimimal reproducible example

A new, **public** GitHub repo is the best place to host your minimal reproducible example. 

[^1]: the below guidance was adapted [from this language](https://github.com/renovatebot/renovate/blob/main/docs/development/minimal-reproductions.md)
