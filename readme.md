# papermaker

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
- `width`
- `height`
- `position`
- `sidecaption`
- `sidecaptionwidth`
