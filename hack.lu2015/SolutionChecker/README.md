#Hack.lu CTF 2015
##Solution Checker
After running this binary, it will give you a list of tasks. You can choose one and input the solution then it will tell you it's right or wrong. The last task is the flag.

So we need to know how our inputs are checked. It's easy to find that there are some weird strings begin with `ERCP` around `off_413f30` near the task descripitions. But checking function `sub_4011c0` is too complicated to reverse directly.

The answers for all the tasks except flag is quiet straightforword and we can guess some of them. For example, 42 for task 3. During the debug we see how they are compared with input and figure out `loc_401250` is a important position. It do the dispatch according to the `ERCP` strings we mentioned above.

With a breakpoint here, we can examine the check process clearly. Symbol `0x1c` means your input should match a given character, `0x0c` skip one char forward, and so on. But soon we find special symbols `0x58` and `0x59`, which called `sub_4011c0` again with a substructure for check, and after a successful subcheck for `0x59` the check process failed.

After a few tests I find the subcheck for `0x58` and `0x59` nearly do the same thing, and these two symbols are dispatched differently, maybe one should pass the check while the other __should not__.

This is the critical point for these reverse, I think, and the remaining part is just some dirty works to recover the flag one-by-one. Sadly I never expect the flag to be so looooooooooooooooooooooooooooooooooong. When I realize I should automate the recovery it's already too late.

By the way, one of the tasks tells me not to use Wikipedia, so I searched `ERCP` but found nothing interesting. If one can consider about the endian issue and search `PCRE`, this job would be mush easier. 