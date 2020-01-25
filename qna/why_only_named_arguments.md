# Why only named arguments?
---
By having only named arguments gives me the ability to add custom error handling for any kind of error.

This involves:
* Wrong argument name
* Wrong argument type
* Wrong argument type
* Required argument not passed
* Not valid **adding_action**, **loading_action** and **action_type** option
* Not valid **hash_formula**
* Not valid directory

I could add positional arguments and have a function that checks every one of them but this would be extremely complicated and code-repetitive and every time I wanted to add a new argument I'll had to re-write the whole checking system.
