# py-teststand

[![PyPI version](https://img.shields.io/pypi/v/py-teststand.svg)](https://pypi.org/project/py-teststand/)
[![Python versions](https://img.shields.io/pypi/pyversions/py-teststand.svg)](https://pypi.org/project/py-teststand/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OS](https://img.shields.io/badge/OS-Windows-0078D4.svg?logo=windows)](https://www.microsoft.com/windows)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/badge/uv-managed-black?logo=uv)](https://github.com/astral-sh/uv)
[![ty](https://img.shields.io/badge/ty-checked-blue?logo=python)](https://github.com/astral-sh/ty)
[![TestStand 2016-2026](https://img.shields.io/badge/TestStand-2016--2026-orange.svg)](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html)
[![Downloads](https://static.pepy.tech/badge/py-teststand)](https://pepy.tech/projects/py-teststand)

[ni-teststand-api-reference]: https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html

Community object-oriented Python 3 bindings (twin API) for the [National Instruments TestStand™ COM API][ni-teststand-api-reference].

## Table of Contents

- [py-teststand](#py-teststand)
  - [Table of Contents](#table-of-contents)
  - [📖 Overview](#-overview)
    - [📛 Name](#-name)
  - [⚠️Transparency](#️transparency)
  - [🚧 Project Status](#-project-status)
    - [🤖 AI-Assisted Development](#-ai-assisted-development)
  - [⚡ Quick Start](#-quick-start)
  - [✨ Features](#-features)
  - [🚀 Installation](#-installation)
    - [⚡ uv](#-uv)
    - [📦 pip](#-pip)
  - [🔗 Compatibility](#-compatibility)
  - [🎯 Design Goals](#-design-goals)
  - [🛠️ Implementation Notes](#️-implementation-notes)
    - [⚙️ Type Library Generation](#️-type-library-generation)
  - [🧰 Technical Stack](#-technical-stack)
  - [🤝 Contributing](#-contributing)
  - [📈 Popularity Over Time](#-popularity-over-time)
  - [⚖️ Legal](#️-legal)

---

## 📖 Overview

`py-teststand` exposes the [TestStand™ COM API][ni-teststand-api-reference] 
as an object-oriented Python interface via [pywin32](https://pypi.org/project/pywin32/).

### 📛 Name

The package is named `py-teststand` (with a dash) to avoid naming collision with the
[pytest testing framework](https://pytest.org/) and for easier relation to the
TestStand™ test executive. The import name uses an underscore: `py_teststand`.

---

## ⚠️Transparency

## 🚧 Project Status

This is a hobby project, maintained on a best-effort basis and **not** yet
under active full-time development ahead of the first release. There is no fixed release
schedule or formal support, but feel free to get in touch.

Treat it as experimental: wrapper behaviour may change between releases without notice 
(like error catching or high level imports).

If you hit a missing TestStand™ binding, a wrong type annotation, or unexpected
TestStand™ COM dispatch behavior, open an issue with a reproducible case. That is the
best way to get it fixed.

For now i prefer lightweight tags based releases (i protected them in repository settings)
instead of fully described ones until reach 1.0.0 release.

### 🤖 AI-Assisted Development

This project leverages Large Language Models (LLMs) to assist with:

- **Codebase audits** and refactoring.
- **Test coverage analysis** and generation.
- **Documentation drafting**.

This is an independent community project. These AI tools are used to optimize
productivity and are **not** an official component of the project, nor do they integrate
with or replace the official
[NIGEL™ AI Advisor](https://www.ni.com/en/support/software-support/nigel-ai.html)
provided by National Instruments. All generated code is manually reviewed by the
maintainer to ensure it meets the project's quality standards.

---

## ⚡ Quick Start

```python
from py_teststand import Engine

with Engine() as engine:
    with engine.get_sequence_file("my_test.seq") as sequence_file:
        with engine.new_execution(sequence_file, "MainSequence") as execution:
            execution.wait_for_end_ex(-1)
            print(f"Result: {execution.result_status}")
```

To see the full capabilities, run the examples suite:

```powershell
uv run .\examples\launch_all_examples.py
```

```python
EXAMPLES: list[tuple[str, str]] = [
    ("station_options_update", "Set station and debug options. Start here."),
    ("search_directory_manage", "Manage TestStand search directories."),
    ("variables_manage", "Create variables across scopes, then retype and remove one."),
    ("data_type_manage", "Create and evolve custom data types (container + strict enum)."),
    ("property_object_serialize", "Dump variables and typedefs to JSON and back."),
    ("sequence_build", "Build a sequence file with steps and save it."),
    ("step_insert", "Insert a step into the sequence sequence_build made."),
    ("step_insert_from_template", "Add a step from a step-type template."),
    ("analyzer_step_name_length", "Walk a sequence and report on its step names."),
    ("workspace_create", "Create a workspace and project file."),
    ("users_manage", "Create users and set their privileges."),
    ("execution_run_test_headless", "Run real pass/fail tests and read their numeric results."),
    ("ui_messages_handle", "Receive UI messages from a running sequence without a GUI."),
    ("result_list_parse", "Parse a sequence execution's ResultList array."),
    (
        "execution_run_subsequence",
        "Run a sequence and read its results. Last; it shuts the engine down.",
    ),
]
```

> ℹ️ A live TestStand™ installation is only required at runtime when COM objects are
> actually instantiated — not at import time.

---

## ✨ Features

- 🐍 **Pythonic attribute access**: TestStand™ COM properties are accessible via
  standard Python attribute notation instead of raw `Dispatch` calls.
- 🏷️ **Type annotations**: All public members carry type hints compatible with
  [ty](https://github.com/astral-sh/ty).
- ⚙️ **TestStand™ station options provisioning**: Read and write TestStand™
  station-level configuration suitable for use in automated deployment pipelines
  (like test-station install scripts).
- 🪶 **Minimal binding surface**: No behavior is added beyond what the TestStand™ COM
  layer provides. Error conditions follow the [TestStand™ COM API contract][ni-teststand-api-reference].
- 🗂️ **Domain-grouped modules**: Classes are organized by TestStand™ domain area for
  easier navigation without adding abstraction or reinterpreting behavior.
- ⚡ **No live TestStand™ installation required at import time**: The committed pywin32
  dispatch cache allows the library to be imported and partially used (type checking,
  configuration building) without a TestStand™ installation present.

---

## 🚀 Installation

### ⚡ uv

```powershell
uv add py-teststand
```

### 📦 pip

```powershell
pip install py-teststand
```

---

## 🔗 Compatibility

| Component                                              | Versions                                                                                      |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| **[Windows](https://www.microsoft.com/en-us/windows)** | 7 to 11                                                                                       |
| **[Python](https://www.python.org/downloads/)**        | 3.8 to 3.14                                                                                   |
| **[TestStand™][ni-teststand-api-reference]**           | [2016 to 2026](https://www.ni.com/docs/en-US/bundle/teststand/page/year-based-and-major.html) |

> ℹ️ Older TestStand™ engine versions may also work if the underlying COM interfaces
> have not changed, but they were not explicitly tested.

---

## 🎯 Design Goals

- 🐍 **Python 3.8 minimum**: Python 3.8 is the last CPython release with official
  Windows 7 support, making it suitable for long-lifecycle, air-gapped manufacturing
  environments where OS upgrades are not feasible. This lets you adopt Python-based
  automation incrementally on existing TestStand™ station hardware.
- ⚙️ **TestStand™ station options as code**: The [TestStand™ Station Options][ni-teststand-api-reference]
  object model is fully exposed, so search directories, model paths, station globals,
  and result processing configuration can be read and written programmatically. This
  makes station configuration reproducible and suitable for provisioners such as:
  - [Terraform](https://developer.hashicorp.com/terraform) - via custom provider / local module (like wrapped PowerShell ones).
  - [Ansible](https://www.ansible.com/)
  - Custom deployment scripts.
- 📄 **No TestStand™ documentation mirroring**: The library does **not** duplicate or
  paraphrase the [official TestStand™ API reference][ni-teststand-api-reference] in its docstrings.
  Reproducing NI's documentation risks creating a secondary source that drifts from the
  official spec over time. For authoritative descriptions of COM objects, properties,
  and method semantics, refer directly to the [TestStand™ API Reference][ni-teststand-api-reference].

---

## 🛠️ Implementation Notes

### ⚙️ Type Library Generation

Python class stubs and interface definitions are generated from the TestStand™
[COM Type Library](https://learn.microsoft.com/en-us/windows/win32/com/type-libraries-and-the-component-object-model)
(`.tlb`) using [pywin32's](https://pypi.org/project/pywin32/)
[`makepy`](https://github.com/mhammond/pywin32/blob/main/com/win32com/client/makepy.py)
utility. The generated output is cached as a
[pywin32 dispatch cache](https://mhammond.github.io/pywin32/) module and checked into
the repository, meaning a live TestStand™ installation is not required at import time —
only at runtime when TestStand™ COM objects are actually instantiated.

The generation process follows this pipeline:

1. 🔍 **TLB introspection**: `makepy` reads the registered TestStand™ COM type library
   via the Windows registry and reflects all exposed interfaces, `CoClass` definitions,
   enumerations, and dispatch IDs.
2. 💾 **Cache dump**: The reflected metadata is serialized into a Python module stored
   under `win32com/gen_py/`, keyed by the TestStand™ type library GUID and version.
   This cache is committed to the repository so users do not need to run `makepy`
   themselves.
3. 🧩 **Wrapper generation**: `py-teststand` classes are authored on top of the cached
   dispatch definitions, adding Python type annotations and translating raw COM
   `VARIANT` and `IDispatch` returns into typed Python objects where applicable.

The bindings stay compatible across TestStand™ engine versions by tracking the stable,
long-lived COM interfaces that exist across the supported range.

---

## 🧰 Technical Stack

| Tool                                             | Purpose                                                     |
| ------------------------------------------------ | ----------------------------------------------------------- |
| **[uv](https://github.com/astral-sh/uv)**        | Python package and project manager                          |
| **[ty](https://github.com/astral-sh/ty)**        | Static type checker for interface validation                |
| **[ruff](https://github.com/astral-sh/ruff)**    | Linter and code formatter (with strict rules)               |
| **[pytest](https://pytest.org/)**                | Unit and integration test runner                            |
| **[pywin32](https://pypi.org/project/pywin32/)** | Windows COM dispatch layer and TestStand™ TLB introspection |

---

## 🤝 Contributing

Bug reports, feature requests, and pull requests are welcome via
[GitHub Issues](https://github.com/TheDomcio/py-teststand/issues).

If you are working with the TestStand™ COM API and have improvements, fixes, or
additional bindings, contributions are encouraged and will be reviewed. See
[CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

---

## 📈 Popularity Over Time

[![Star History Chart](https://api.star-history.com/svg?repos=TheDomcio/py-teststand&type=Date)](https://star-history.com/#TheDomcio/py-teststand&Date)

---

## ⚖️ Legal

TestStand™ is a registered trademark of
[National Instruments Corporation](https://www.ni.com). Refer to
[NI's TestStand™ licensing options](https://www.ni.com/en/shop/teststand.html) for
information on required licenses to operate the TestStand™ engine.

`py-teststand` is an independent community project and is not affiliated with, endorsed
by, or maintained by National Instruments or its parent company
[Emerson](https://www.emerson.com). References to the [TestStand™ API][ni-teststand-api-reference] are made
solely for interoperability purposes.
