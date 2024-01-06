# papermaker (work in progress)

Typeset professional-quality scientific articles from mostly-Markdown sources, retaining the ability to use LaTeX.

Key features are:

- separation of content (source files) and formatting (template)
- high-quality typography
- use Markdown format by default, keeping the option to use LaTeX whenever needed
- Markdown source text should be easily reused and/or shared with coauthors
- define metadata (title, authors, affiliations...) only once, all in a single `toml` file
- use LaTeX for inline math expressions and numbered or unnumbered equations
- use simple 'toml' syntax to specify floating figures and tables
- use (simple) LaTeX syntax for referencing figures, tables, sections, equations or page numbers
- use (simple) LaTeX commands to insert in-text citations defined in a separate BibTeX file, with the list of references being generated automatically
- define references in a BiBTeX file (e.g., exported from Zotero)
- optionally define custom LaTeX commands and/or document-wide text substitutions (e.g., convert `δ13C` in source to δ<sup>13</sup>C in the final PDF)

The core idea behind `papermaker` is that *writing* LaTeX is not particularly hard using modern implementations like XeLaTeX, which use UTF-8 encoding by default. It is usually much more challenging/time-consuming to fine-tune the final document's format by fiddling with the LaTeX source. On the other hand, it is much easier to share/re-use text writtent in Markdown than LaTeX. `papermaker` thus uses Markdown by default, keeping the considerable power of LaTeX available where needed, and hides the complex LaTeX syntax for important constructs such as floating figures behind a simpler syntax.

# Installation and usage

This is an early-stage work in progress. For now, you need to install a LaTeX distribution and the other dependencies are handled by [pixi](https://pixi.sh).

* Install [TeX Live](https://www.tug.org/svn/texlive) (on a Mac, your best option is [MacTeX](http://www.tug.org/mactex))
* Install pixi (instructions [here](https://pixi.sh))
* From `papermaker`'s root directory, `pixi run build` should process your paper, installing the required dependencies as needed in the fist run.
* When building an article, `papermaker` looks for source files in `src`, and the output is saved to `build`.

# Source files

## Metadata

Metadata such as authors' names, emails, ORCIDs, institutions, or the article's title, are defined in `src/metadata.toml`.

```
title = 'The title of the paper'

[[author]]
name = 'J. Smith'
affiliations = 'USS'
email = 'john.smith@server.net'
orcid = '0000-0000-000-000'
corresponding = true

[[author]]
name = 'J. Doe'
affiliations = ['AFA', 'USS']
email = 'jane.doe@server.net'

[affiliations]
USS = "University of Scientific Studies"
AFA = "Academy of the Fine Arts"
```

## Text

The body of the article is typeset based on the contents of `src/body.md`.
Other parts of the document are from `src/abstract.md`,  `src/contributions.md`,  `src/acknowledgements.md`, and  `src/reproducibility.md`.

## Figures

Figures are stored in `src/figures`. Each figure is defined by two files:

- a single PDF file, with a `.pdf` extension, corresponding to the contents of the figure (e.g., a picture or a plot)
- a single Markdown file, with a `.md` extension, corresponding to the caption for this figure.

For example, `src/figures` may contain:

```
src
└── figures
    ├── age-plot.md
    ├── age-plot.pdf
    ├── field-photos.md
    └── field-photos.md
```

In `src/body.md`, you may insert a figure such as fig. \ref{fig:field-photos} using simple `toml` syntax enclosed in at least three backticks:

```
[figure]
name = 'field-photos'
label = 'fig:field-photos'
position = 'b!'
```

The `name` attribute is mandatory and must correspond to a pair of files in `src/figures`.
Other possible attributes are:

- `label`: used to reference the figure number elsewhere in the text: `Fig. \ref{fig:field-photos}` will be typeset as “Fig. \ref{fig:field-photos}”. You may use a non-breakable space (`alt-space` on a Mac) before the `\ref` command.
- `width`: specify the printed width of the figure; may be anything that LaTeX understand (e.g., `10cm`; `80mm`; `4in`; `0.8\textwidth`...).
- `height`: specify the printed height of the figure; may be anything that LaTeX understand.
- `position`: specify the desired position of the floating figure; you may use any combination of the following parameters:


| Parameter | Position |
|:---------:|:---------|
| h         | Place the float here, i.e., approximately at the same point it occurs in the source text (however, not exactly at the spot) |
| t         | Position at the top of the page. |
| b         | Position at the bottom of the page. |
| p         | Put on a special page for floats only. |
| !         | Override internal parameters LaTeX uses for determining "good" float positions. |

- `sidecaption`: if this keyword is present and set to one of `"right"`, `"left"`, `"r"`, or `"l"`, the caption will be typeset on the side rather than at the bottom of the figure.
- `sidecaptionwidth`: specify the width fraction used up by the side caption (default is `0.5`).

## Tables

## Custom commands

You may define \LaTeX{} commands either in `src/preamble.tex`  or at the top of `src/body.md`,  using `\newcommand{}`, e.g.:

```
\newcommand{\foo}{FOO}
\newcommand{\degC}[1]{\,°C}
```

Thereafter, `\foo{}` in the source will be typeset as “FOO” and `37.2\degC{}` as “37.2 °C”.

## Citations

You may cite references defined in the BibTeX file `src/refs.bib` using the following commands:

- `\cite{foo}` with be typeset as “[X]” (where X is a integer incremented with each new citation).
- `\namecite{foo}` with be typeset as “Foo et al. [X]”

## Equations

Numbered equations follow LaTeX syntax, using either UTF encoding (e.g `δ`) or LaTeX commands (e.g., `\delta`):

```
\begin{equation}
\sigma = \sum_i4\cdot α^2_i
\label{eq:foo}
\end{equation}
```

Unnumbered equations use LaTeX math's display mode:

```
\[
\sigma = \sum_i4\cdot α^2_i
\]
```

Which should be rendered as:

\[
\sigma = \sum_i4\cdot α^2_i
\]
