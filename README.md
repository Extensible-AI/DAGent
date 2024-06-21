# DAGent
Agentic behavior as DAGs

## TODOs
- [ ] Look if things run in memory and how to isolate for large workflows -> e.g. funcA(funcB(...)) -> funcA(...) -> funcB(...)
- [ ] Creating a data model for communication between functions -> autogenerate?
- [ ] Logging
- [ ] Alerting on error
- [x] Add a compile method to derive data models and tool descriptions

## Notes
Some issues i am noticing:
- tools are very finnicky, one letter off and the lookup can be wrong
- tool descriptions must be good for the llm to be able to figure out what to run
- writing the tool itself is icky
- passing params/overriding args and what that should look like might need to be smth with dataclass or pydantic tbd
- compile call to derive the data models
- there is an inherent development flow to be followed for communication standard
- imo some of this could be abstracted away, while keeping it light
