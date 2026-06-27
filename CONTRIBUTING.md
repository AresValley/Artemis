<!-- omit in toc -->
# Contributing to Artemis

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions.

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
  - [Local Setup](#local-setup)
  - [Sync your local repository](#sync-your-local-repository)
  - [Create a dedicated branch](#create-a-dedicated-branch)
  - [Set up the development environment](#set-up-the-development-environment)
  - [Develop your changes](#develop-your-changes)
  - [Submitting Your Contribution](#submitting-your-contribution)
- [Join The Project Team](#join-the-project-team)

## Code of Conduct

This project and everyone participating in it is governed by the
[Artemis Code of Conduct](https://github.com/AresValley/Artemis/blob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <aresvalley.info@gmail.com>.

## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://aresvalley.github.io/Artemis/).

Before you ask a question, it is best to search for existing [Issues](https://github.com/AresValley/Artemis/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/AresValley/Artemis/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://aresvalley.github.io/Artemis/). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/AresValley/Artemis/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to <aresvalley.info@gmail.com>.

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/AresValley/Artemis/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Artemis, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://aresvalley.github.io/Artemis/) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/AresValley/Artemis/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/AresValley/Artemis/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux. <!-- this should only be included if the project has a GUI -->
- **Explain why this enhancement would be useful** to most Artemis users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

## Your First Code Contribution

To start contributing code to Artemis, you'll need to set up your local development environment. We use [uv](https://docs.astral.sh/uv/) for fast, reliable dependency and environment management, which relies on the `pyproject.toml` file.

### Local Setup

1. Go to <https://github.com/AresValley/Artemis> and click the **Fork** button in the top-right corner to create your own copy of the project repository.
1. Clone **your** fork to your local computer (replace `<<YOUR-USERNAME>>` with your actual GitHub username):

    ```bash
    git clone https://github.com/<<YOUR-USERNAME>>/Artemis
    cd Artemis
    ```

1. Add the original repository as the `upstream` remote to keep your fork synchronized with the project:

    ```bash
    git remote add upstream https://github.com/AresValley/Artemis.git
    ```

1. Install uv: If you haven't already, install uv via your preferred package manager or the official installer from the official website [uv](https://docs.astral.sh/uv/)

### Sync your local repository

Update your local `main` branch with the latest changes from the upstream repository:

```bash
git checkout main
git pull upstream main
```

Optionally, keep your fork up to date as well:

```bash
git push origin main
```

### Create a dedicated branch

Create a new branch **from the updated `main` branch** using a short, descriptive name:

```bash
git checkout -b <branch-name>
```

### Set up the development environment

Run the following command from the project root. `uv` will automatically create the virtual environment (if needed) and install all the dependencies defined in `pyproject.toml`.

```bash
uv sync
```

Activate the virtual environment with:

- Linux/macOS: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

### Develop your changes

Commit your work regularly as you make progress. A typical workflow is:

```bash
git add .
git commit -m "Describe your changes"
```

For example:

```bash
git commit -m "Add support for custom configuration"
```

Try to:

- Make small, focused commits.
- Write clear and descriptive commit messages.
- Keep your branch focused on a single feature or bug fix.

### Submitting Your Contribution

Once your changes are complete and have been tested locally, push your branch to your fork:

```bash
git push origin <branch-name>
```

Then:

1. Open your fork on GitHub.
1. Click the **Compare & pull request** button that appears.
1. Write a clear Pull Request title and description explaining:
   - what changed;
   - why it changed;
   - how you tested it.
1. Submit the Pull Request. A maintainer will review your Pull Request.

## Join The Project Team

If you are a frequent contributor and show long-term commitment to the Artemis project, the core maintainers may invite you to join the official project team.

As a team member, you will help review Pull Requests, manage issues, and shape the future roadmap of Artemis. Keep contributing, helping out in discussions, and being an active part of our community!
