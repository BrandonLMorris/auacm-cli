# auacm-cli changelog

## 0.4

**Fixes**
- Actually support Python 2 (not included tests)


**Features**
- `problem-info` output formatted to 80 characters long with word wrapping
- `init` subcommand: create a directory for a problem with description,
sample cases, etc.
- `test` subcommand: execute a solution against the sample cases. Can pull
cases from the server or use local (custom) cases
- `scoreboard` subcommand: display the scoreboard of a competition


**Changes**
- `test` subcommand changed to `ping`
