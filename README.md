# py-teststand

Community object-oriented Python 3 bindings for the [National Instruments TestStand™ COM API](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html).

> ⚠️ **Early Implementation Stage** — Consider as experimental. Interfaces may change between releases without prior notice.
> 🤖 **AI Disclaimer**: This project uses LLMs for codebase and coverage audits and does not replace or integrate with the [NIGEL™ AI Advisor](https://www.ni.com/en/support/software-support/nigel-ai.html).

## 📖 Overview

`py-teststand` exposes the [TestStand™ COM API](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html) as an object-oriented Python interface via [pywin32](https://pypi.org/project/pywin32/).

### 📛 Name

The package is named `py-teststand` (with a dash) to avoid naming collision with the [pytest testing framework](https://pytest.org/) and for easier relation to TestStand™ test executive.

---

## 🚧 Project Status

`py-teststand` is a hobby project maintained on a best-effort basis
and is **not** under active full-time development (for first release).
There are no guaranteed scheduled release cadences or support (but feel free to contact).

That said:

- 🐛 **Bug reports and feature requests** are welcome via [GitHub Issues](https://github.com/TheDomcio/py-teststand/issues).
- 🤝 **Pull requests** are welcomed and reviewed. If you are working with the TestStand™ COM API and have improvements, fixes, or additional bindings, contributions are encouraged.

If you encounter a missing TestStand™ binding, an incorrect type annotation, or unexpected TestStand™ COM dispatch behavior, opening an issue with a reproducible case is the most effective way to get it addressed, I will try to investigate and find solution as fast as possible.

---

## 🛠️ Implementation Notes

### ⚙️ Type Library Generation

Python class stubs and interface definitions are generated from the TestStand™ [COM Type Library](https://learn.microsoft.com/en-us/windows/win32/com/type-libraries-and-the-component-object-model) (`.tlb`) using [pywin32's](https://pypi.org/project/pywin32/) [`makepy`](https://github.com/mhammond/pywin32/blob/main/com/win32com/client/makepy.py) utility. The generated output is cached as a [pywin32 dispatch cache](https://mhammond.github.io/pywin32/) module and checked into the repository, meaning a live TestStand™ installation is not required at import time — only at runtime when TestStand™ COM objects are actually instantiated.

The generation process follows this pipeline:

1. 🔍 **TLB introspection** — `makepy` reads the registered TestStand™ COM type library via the Windows registry and reflects all exposed interfaces, `CoClass` definitions, enumerations, and dispatch IDs.
2. 💾 **Cache dump** — The reflected TestStand™ metadata is serialized into a Python module stored under `win32com/gen_py/`, keyed by the TestStand™ type library GUID and version. This cache is committed to the repository so users do not need to run `makepy` themselves.
3. 🧩 **Wrapper generation** — `py-teststand` classes are authored on top of the cached TestStand™ dispatch definitions, adding Python type annotations and translating raw COM `VARIANT` and `IDispatch` returns into typed Python objects where applicable.

This approach means the bindings target a specific version of the TestStand™ type library. Compatibility across TestStand™ engine versions is maintained by keeping the wrapper surface aligned with stable, long-lived TestStand™ COM interfaces present across the supported version range.

---

## 🎯 Design Goals

- 🐍 **Python 3.8 minimum** — Python 3.8 (uv supports / distributes even 3.8.20) is the last CPython release with official Windows 7 support. Many manufacturing and test environments run long-lifecycle OS images on air-gapped station hardware where upgrading the OS is not feasible on short timescales. Maintaining a 3.8-compatible codebase allows incremental adoption of Python-based automation on existing TestStand™ station hardware without requiring a platform migration first.
- ⚙️ **TestStand™ station options as code** — The [TestStand™ Station Options](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html) object model is fully exposed, allowing TestStand™ search directories, model paths, station globals, and result processing configuration to be read and written programmatically. This makes TestStand™ station configuration reproducible and suitable for provisioners such as [Ansible](https://www.ansible.com/), [Chef](https://www.chef.io/), or custom deployment scripts — replacing manual point-and-click TestStand™ setup with version-controlled configuration.
- 📄 **No TestStand™ documentation mirroring** — The library does **not** duplicate or paraphrase the [official TestStand™ API reference](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html) in its docstrings, as eproducing NI's documentation would introduce a secondary source that diverges from the official TestStand™ spec as new versions evolve, creating a risk of misinformation, therefore for authoritative descriptions of TestStand™ COM objects, properties, method parameters, and return value semantics etc. refer directly to the [TestStand™ API Reference](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html).

---

## 🧰 Technical Stack

| Tool                                             | Purpose                                                     |
| ------------------------------------------------ | ----------------------------------------------------------- |
| **[uv](https://github.com/astral-sh/uv)**        | Python package and project manager                          |
| **[ty](https://github.com/astral-sh/ty)**        | Static type checker for interface validation                |
| **[ruff](https://github.com/astral-sh/ruff)**    | Linter and code formatter                                   |
| **[pytest](https://pytest.org/)**                | Unit and integration test runner                            |
| **[pywin32](https://pypi.org/project/pywin32/)** | Windows COM dispatch layer and TestStand™ TLB introspection |

---

## 🔗 Compatibility

| Component                                                                                                               | Versions     |
| ----------------------------------------------------------------------------------------------------------------------- | ------------ |
| **[Windows](https://www.microsoft.com/en-us/windows)**                                                                  | 7 — 11       |
| **[Python](https://www.python.org/downloads/)**                                                                         | 3.8 — 3.14   |
| **[TestStand™](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html)** | 2016 — 2026+ |

> ℹ️ Older TestStand™ engine versions may also work if the underlying TestStand™ COM interfaces have not changed, but they were not explicitly tested.

---

## ✨ Features

- 🐍 **Pythonic attribute access** — TestStand™ COM properties are accessible via standard Python attribute notation instead of raw `Dispatch` calls.
- 🏷️ **Type annotations** — All public members carry type hints compatible with [ty](https://github.com/astral-sh/ty).
- ⚙️ **TestStand™ station options provisioning** — Read and write TestStand™ station-level configuration suitable for use in automated deployment pipelines (like test stations install scripts).
- 🪶 **Minimal binding surface** — No behavior is added beyond what the TestStand™ COM layer provides. Edge cases and error conditions follow the TestStand™ COM API contract documented in the [official TestStand™ reference](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html). The binding layer is intentionally lightweight and not overcommented, signatures and object hierarchy map directly to the TestStand™ COM API without adding abstraction or reinterpreting behavior (but modules themselves are sorted under domains for easier management).
- ⚡ **No live TestStand™ installation required at import time** — The committed pywin32 dispatch cache allows the library to be imported and partially used (type checking, configuration building) without a TestStand™ installation present.

---

## 🚀 Installation

### 📦 pip

```powershell
pip install py-teststand

```

### ⚡ uv

```powershell
uv pip install py-teststand

```

---

## 📈 Popularity Over Time

---

## ⚖️ Legal

TestStand™ is a registered trademark of [National Instruments Corporation](). Refer to [NI's TestStand™ licensing options]() for information on required licenses to operate the TestStand™ engine.

`py-teststand` is an independent community project and is not affiliated with, endorsed by, or maintained by National Instruments or its parent company [Emerson](). References to the TestStand™ API are made solely for interoperability purposes.
