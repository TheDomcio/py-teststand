# py-teststand

Community object-oriented Python 3 bindings (twin API) for the [National Instruments TestStand™ COM API](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html).

> ⚠️ **Early Implementation Stage**: Treat it as experimental. Interfaces may change between releases without notice.
> 🤖 **AI Disclaimer**: This project uses LLMs for codebase and coverage audits and does not replace or integrate with the [NIGEL™ AI Advisor](https://www.ni.com/en/support/software-support/nigel-ai.html).

## 📖 Overview

`py-teststand` exposes the [TestStand™ COM API](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html) as an object-oriented Python interface via [pywin32](https://pypi.org/project/pywin32/).

### 📛 Name

The package is named `py-teststand` (with a dash) to avoid naming collision with the [pytest testing framework](https://pytest.org/) and for easier relation to TestStand™ test executive.

---

## 🚧 Project Status

`py-teststand` is a hobby project, maintained on a best-effort basis and
**not** yet under active full-time development ahead of the first release.
There is no fixed release schedule or formal support, but feel free to get in touch.

That said:

- 🐛 **Bug reports and feature requests** are welcome via [GitHub Issues](https://github.com/TheDomcio/py-teststand/issues).
- 🤝 **Pull requests** are welcomed and reviewed. If you are working with the TestStand™ COM API and have improvements, fixes, or additional bindings, contributions are encouraged.

If you hit a missing TestStand™ binding, a wrong type annotation, or unexpected TestStand™ COM dispatch behavior, open an issue with a reproducible case. That is the best way to get it fixed, and I will investigate and try to find a solution as fast as I can.

---

## 🛠️ Implementation Notes

### ⚙️ Type Library Generation

Python class stubs and interface definitions are generated from the TestStand™ [COM Type Library](https://learn.microsoft.com/en-us/windows/win32/com/type-libraries-and-the-component-object-model) (`.tlb`) using [pywin32's](https://pypi.org/project/pywin32/) [`makepy`](https://github.com/mhammond/pywin32/blob/main/com/win32com/client/makepy.py) utility. The generated output is cached as a [pywin32 dispatch cache](https://mhammond.github.io/pywin32/) module and checked into the repository, meaning a live TestStand™ installation is not required at import time, only at runtime when TestStand™ COM objects are actually instantiated.

The generation process follows this pipeline:

1. 🔍 **TLB introspection**: `makepy` reads the registered TestStand™ COM type library via the Windows registry and reflects all exposed interfaces, `CoClass` definitions, enumerations, and dispatch IDs.
2. 💾 **Cache dump**: The reflected TestStand™ metadata is serialized into a Python module stored under `win32com/gen_py/`, keyed by the TestStand™ type library GUID and version. This cache is committed to the repository so users do not need to run `makepy` themselves.
3. 🧩 **Wrapper generation**: `py-teststand` classes are authored on top of the cached TestStand™ dispatch definitions, adding Python type annotations and translating raw COM `VARIANT` and `IDispatch` returns into typed Python objects where applicable.

This approach means the bindings target a specific version of the TestStand™ type library. The bindings stay compatible across TestStand™ engine versions by tracking the stable, long-lived COM interfaces that exist across the supported range.

---

## 🎯 Design Goals

- 🐍 **Python 3.8 minimum**: Python 3.8 (uv supports and distributes even 3.8.20) is the last CPython release with official Windows 7 support. Many manufacturing and test environments run long-lifecycle OS images on air-gapped station hardware where upgrading the OS is not feasible on short timescales. A 3.8-compatible codebase lets you adopt Python-based automation incrementally on existing TestStand™ station hardware without migrating the platform first.
- ⚙️ **TestStand™ station options as code**: The [TestStand™ Station Options](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html) object model is fully exposed, so TestStand™ search directories, model paths, station globals, and result processing configuration can be read and written programmatically. This makes station configuration reproducible and suitable for provisioners such as [Ansible](https://www.ansible.com/), [Chef](https://www.chef.io/), or custom deployment scripts. It replaces manual point-and-click setup with version-controlled configuration.
- 📄 **No TestStand™ documentation mirroring**: The library does **not** duplicate or paraphrase the [official TestStand™ API reference](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html) in its docstrings. Reproducing NI's documentation would create a secondary source that drifts from the official TestStand™ spec as new versions ship, which risks spreading misinformation. For authoritative descriptions of TestStand™ COM objects, properties, method parameters, and return value semantics, refer directly to the [TestStand™ API Reference](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html).

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

| Component                                                                                                               | Versions      |
| ----------------------------------------------------------------------------------------------------------------------- | ------------- |
| **[Windows](https://www.microsoft.com/en-us/windows)**                                                                  | 7 to 11       |
| **[Python](https://www.python.org/downloads/)**                                                                         | 3.8 to 3.14   |
| **[TestStand™](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html)** | 2016 to 2026+ |

> ℹ️ Older TestStand™ engine versions may also work if the underlying TestStand™ COM interfaces have not changed, but they were not explicitly tested.

---

## ✨ Features

- 🐍 **Pythonic attribute access**: TestStand™ COM properties are accessible via standard Python attribute notation instead of raw `Dispatch` calls.
- 🏷️ **Type annotations**: All public members carry type hints compatible with [ty](https://github.com/astral-sh/ty).
- ⚙️ **TestStand™ station options provisioning**: Read and write TestStand™ station-level configuration suitable for use in automated deployment pipelines (like test-station install scripts).
- 🪶 **Minimal binding surface**: No behavior is added beyond what the TestStand™ COM layer provides. Edge cases and error conditions follow the TestStand™ COM API contract documented in the [official TestStand™ reference](https://www.ni.com/docs/en-US/bundle/teststand-api-reference/page/tshelp/teststand-api-reference.html). The binding layer is intentionally lightweight and not overcommented. Signatures and the object hierarchy map directly to the TestStand™ COM API without adding abstraction or reinterpreting behavior (modules are grouped by domain for easier navigation).
- ⚡ **No live TestStand™ installation required at import time**: The committed pywin32 dispatch cache allows the library to be imported and partially used (type checking, configuration building) without a TestStand™ installation present.

---

## 🚀 Installation

### 📦 pip

```powershell
pip install py-teststand

```

### ⚡ uv

```powershell
uv add py-teststand

```

---

## 📈 Popularity Over Time

---

## ⚖️ Legal

TestStand™ is a registered trademark of [National Instruments Corporation](https://www.ni.com). Refer to [NI's TestStand™ licensing options](https://www.ni.com/en/shop/teststand.html) for information on required licenses to operate the TestStand™ engine.

`py-teststand` is an independent community project and is not affiliated with, endorsed by, or maintained by National Instruments or its parent company [Emerson](https://www.emerson.com). References to the TestStand™ API are made solely for interoperability purposes.
