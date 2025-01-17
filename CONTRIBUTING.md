# Contributing to Abstraction Layer in Measurement Plug-In for Python

Contributions to Abstraction Layer in Measurement Plug-In for Python are welcome from all!

Abstraction Layer in Measurement Plug-In for Python is managed via [git](https://git-scm.com), with
the canonical upstream repository hosted on [GitHub](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python).

Abstraction Layer in Measurement Plug-In for Python follows a pull-request model for development. If
you wish to contribute, you will need to create a GitHub account, fork this project, push a
branch with your changes to your project, and then submit a pull request.

Please remember to sign off your commits (e.g., by using `git commit -s` if you
are using the command line client). This amends your git commit message with a line
of the form `Signed-off-by: Name Lastname <name.lastmail@emailaddress.com>`. Please
include all authors of any given commit into the commit message with a
`Signed-off-by` line. This indicates that you have read and signed the Developer
Certificate of Origin (see below) and are able to legally submit your code to
this repository.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/) for more details.

# Getting Started

## Prerequisites

- (Optional) Install [Visual Studio Code](https://code.visualstudio.com/download).
- Install Git.
- Install [Poetry](https://python-poetry.org/docs/#installation). For the recommended Poetry version,
  see [Software and Package Dependencies](README.md#software-and-package-dependencies).
- Install Python and add it to the `PATH`. For the recommended Python version, see
  [Software and Package Dependencies](README.md#software-and-package-dependencies).

## Clone Repo

Clone the repo, this will pull the workflow documentation to create the Abstraction Layer in
Measurement Plug-In for Python measurements and related examples.

```cmd
git clone https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python.git
```

## HAL and FAL Implementation workflow

- Refer to the [HAL in Measurement Plug-in](./docs/HAL%20in%20Measurement%20Plug-In.md) to
  understand the workflow for implementing HAL for measurement plug-ins.
- Refer to the [FAL in Measurement Plug-in](./docs/FAL%20in%20Measurement%20Plug-In.md) to
  understand the workflow for implementing FAL for measurement plug-ins.

# Adding dependencies

Add dependency package for the example measurement plug-in using the [`poetry
add`](https://python-poetry.org/docs/cli/#add) command.

```cmd
poetry add <name_of_dependency>:<version>
```

# Lint Code

To check the code and update it for formatting errors

```cmd
poetry run ni-python-styleguide fix
```

# Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/NI-Measurement-Plug-Ins/abstraction-layer-python/blob/main/LICENSE)
for details about how Abstraction Layer in Measurement Plug-In for Python is licensed.
