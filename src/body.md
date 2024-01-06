# Design goals and philosophy

* separate content (source files) and formatting (template)
* use Markdown format by default, keeping the option to use LaTeX whenever needed
* define metadata (title, authors, affiliations...) only once, all in a single `toml` file
* use LaTeX for inline math expressions and numbered or unnumbered equations
* use simple 'toml' syntax to specify floating figures and tables
* use LaTeX syntax for referencing figures, tables, sections or page numbers
* insert in-text citations defined in a separate BibTeX file, with the list of references being generated automatically
* optionally define custom LaTeX commands and/or document-wide text substitutions

The core idea behind `papermaker` is that *writing* LaTeX is not particularly hard using modern implementations like XeLaTeX, which use UTF-8 encoding by default. It is usually much more challenging/time-consuming to fine-tune the final document's format by fiddling with the LaTeX source. On the other hand, it is much easier to share/re-use text writtent in Markdown than LaTeX. `papermaker` thus uses Markdown by default, keeping the considerable power of LaTeX available where needed, and hides the complex LaTeX syntax for important constructs such as floating figures behind a simpler `toml` syntax.

# Installation and usage

This is an early-stage work in progress. For now, you need to install a LaTeX distribution and the other dependencies are handled by [pixi](https://pixi.sh).

* Install [TeX Live](https://www.tug.org/svn/texlive) (on a Mac, your best option is [MacTeX](http://www.tug.org/mactex))
* Install pixi (instructions [here](https://pixi.sh))
* From `papermaker`'s root directory, `pixi run build` should process your paper, installing the required dependencies as needed in the rist run.
* When building an article, `papermaker` looks for source files in `src`, and the output is saved to `build`.

# Source files

## Metadata
\label{sec:metadata}

Metadata such as authors' names, emails, ORCIDs, institutions, or the article's title, are defined in `src/metadata.toml`.

\vspace{2ex}
\begin{lstlisting}
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
\end{lstlisting}
\vspace{2ex}

## Text

The body of the article is typeset based on the contents of `src/body.md`.
Other parts of the document are from `src/abstract.md`,  `src/contributions.md`,  `src/acknowledgements.md`, and  `src/reproducibility.md`.

## Figures

Figures are stored in `src/figures`.
Each figure is defined by two files:

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

\vspace{2ex}
\begin{lstlisting}
 ```
 [figure]
 name = 'field-photos'
 label = 'fig:field-photos'
 position = 'b!'
 ```
\end{lstlisting}
\vspace{2ex}

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

Figure \ref{fig:field-photos} is an example figure created from the backtick block above.

# Custom commands

You may define \LaTeX{} commands at the top of this source file using `\newcommand{}`:

```
\newcommand{\foo}{FOO}
\newcommand{\degC}[1]{\,°C}
```

Thereafter, `\foo{}` in the source will be typeset as \foo{} and `37.2\degC{}` as 37.2\degC{}.

# Citations

You may cite references defined in the Bib\TeX{} file `src/refs.bib` using the following commands.

Pretium aenean pharetra magna ac placerat vestibulum lectus mauris. Scelerisque varius morbi enim nunc \cite{Coplen-2007}. In vitae turpis massa sed elementum tempus. Et magnis dis parturient montes nascetur. Blandit libero volutpat sed cras ornare arcu dui vivamus. Urna neque viverra justo nec ultrices dui sapien. Purus in mollis nunc sed id semper. Auctor augue mauris augue neque gravida in fermentum et sollicitudin. Fringilla ut morbi tincidunt augue. Nunc mi ipsum faucibus vitae aliquet nec ullamcorper sit. Morbi tincidunt ornare massa eget egestas purus viverra \namecite{Coogan-2019}.

# Methods
\label{sec:methods}

Vitae nunc sed velit dignissim sodales. Mauris a diam maecenas sed. Sed ullamcorper morbi tincidunt ornare massa. Ut diam quam nulla porttitor massa id neque aliquam vestibulum. Massa sapien faucibus et molestie ac feugiat sed. Tortor consequat id porta nibh venenatis cras. Nulla pellentesque dignissim enim sit amet venenatis urna. Viverra nibh cras pulvinar mattis nunc sed. Ac odio tempor orci dapibus ultrices in. Posuere ac ut consequat semper viverra nam libero justo. Enim tortor at auctor urna.

```
import foo
print(foo.bar)
```

Eu augue ut lectus arcu bibendum at varius vel pharetra. Feugiat vivamus at augue eget arcu dictum varius duis. Mattis enim ut tellus elementum sagittis vitae et leo. Ac ut consequat semper viverra nam libero justo laoreet sit. Enim ut tellus elementum sagittis vitae et leo. Amet nisl suscipit adipiscing bibendum est. Non blandit massa enim nec dui nunc mattis enim ut. Tellus elementum sagittis vitae et leo duis ut.

```
[table]
name = 'table-latex'
position = 'b!'
label = 'tab:latex'
```

Amet commodo nulla facilisi (\ref{eq:foo}) nullam vehicula. Congue mauris rhoncus aenean vel elit. Mattis molestie a iaculis at erat pellentesque adipiscing commodo elit. Euismod lacinia at quis risus sed vulputate odio. Lacinia quis vel eros donec ac odio. Mattis pellentesque id nibh tortor id aliquet lectus. Mi proin sed libero enim sed faucibus turpis in. Ut sem viverra aliquet eget sit amet tellus cras. Egestas diam in arcu cursus. Enim ut sem viverra aliquet. Tortor condimentum lacinia quis vel eros donec ac odio tempor. Tellus mauris a diam maecenas sed enim. Mattis molestie a iaculis at erat pellentesque adipiscing commodo elit. Lectus arcu bibendum at varius vel pharetra vel turpis nunc.

```
[figure]
name = 'qmc'
position = 'tb'
label = 'fig:qmc'
width = '\textwidth'
sidecaption = 'right'
sidecaptionwidth = '0.45'
```

# Results

Vivteeerra aliquet iddn section eget sit amet tellus cras. Et netus et malesuada fames axx turpsdis \ref{sec:metadata} egestas. Praesent elementum facilisis leo vel fringilla est. Nullam ac tortor vitae purus faucibus ornare suspendisse sed nisi. Dictum non consectetur a erat nam at lectus urna. Facilisi etiam dignissim diam quis enim lobortis. Magna sit amet purus gravida quis blandit.

```
[table]
name = 'table-pdf'
position = 'b!'
label = 'tab:pdf'
```

Faucibus vitae aliquet nec ullamcorper sit amet risus nullam eget. Ultricies integer quis auctor elit sed vulputate mi. Vestibulum lorem sed risus ultricies tristique. Morbi tristique senectus et netus et malesuada fames. Ultricies lacus sed turpis tincidunt id aliquet risus feugiat in. Et malesuada fames ac turpis egestas maecenas pharetra. Nunc scelerisque viverra mauris in aliquam sem fringilla ut morbi. At risus viverra adipiscing at in tellus integer feugiat scelerisque. Sed ullamcorper morbi tincidunt ornare massa eget egestas purus viverra. Eros in cursus turpis massa tincidunt dui ut.

\begin{equation}
\sigma = \sum_i4\cdot α^2_i
\label{eq:foo}
\end{equation}

Bibendum ut Δ47 tristique et egestas quis. Maecenas volutpat blandit aliquam etiam erat. Velit egestas dui id ornare arcu odio. Commodo ullamcorper a lacus vestibulum sed arcu non odio. Ut lectus arcu bibendum at varius vel. Vitae tortor condimentum lacinia quis. Mattis nunc sed blandit libero volutpat. Dolor sit amet consectetur adipiscing elit duis tristique sollicitudin nibh. Est ullamcorper eget nulla facilisi. In massa tempor nec feugiat nisl pretium fusce. At consectetur lorem donec massa sapien. Dui sapien eget mi proin sed libero enim sed. Eget velit aliquet sagittis id consectetur. A diam sollicitudin tempor id eu nisl. Eleifend quam adipiscing vitae proin. Nunc mattis enim ut tellus elementum sagittis.

# Discussion

Feugiat vivamus at augue eget. In hendrerit gravida rutrum quisque non tellus. Neque vitae tempus quam pellentesque. Porttitor lacus luctus accumsan tortor posuere ac. Egestas sed tempus urna et. Suspendisse ultrices gravida dictum fusce ut placerat orci nulla. Nisl nisi scelerisque eu ultrices vitae auctor eu. Massa eget egestas purus viverra accumsan in. Sit amet justo donec enim diam vulputate ut pharetra. Ullamcorper velit sed ullamcorper morbi tincidunt. Morbi quis commodo odio aenean. Sed adipiscing diam donec adipiscing tristique risus nec.

Elit pellentesque habitant morbi tristique senectus et. Pellentesque nec nam aliquam sem et tortor consequat id porta. Scelerisque viverra mauris in aliquam sem fringilla ut morbi tincidunt. Vitae ultricies leo integer malesuada nunc vel risus commodo. Dignissim convallis aenean et tortor at risus viverra adipiscing. Sit amet justo donec enim. Neque aliquam vestibulum morbi blandit cursus risus. Quis blandit turpis cursus in hac habitasse platea dictumst. Neque aliquam vestibulum morbi blandit cursus risus at. Et malesuada fames ac turpis egestas. Egestas erat imperdiet sed euismod nisi porta lorem. Nisl pretium fusce id velit ut. Nisl condimentum id venenatis a condimentum vitae sapien pellentesque habitant. Vestibulum morbi blandit cursus risus at. Eget sit amet tellus cras adipiscing enim. Proin nibh nisl condimentum id venenatis a condimentum vitae sapien. Viverra nam libero justo laoreet sit amet cursus. Metus aliquam eleifend mi in.

Neque gravida in fermentum et sollicitudin ac. Quam lacus suspendisse faucibus interdum posuere lorem ipsum dolor. Cursus in hac habitasse platea dictumst. Tincidunt tortor aliquam nulla facilisi cras fermentum. Nam libero justo laoreet sit amet cursus. Sed turpis tincidunt id aliquet risus feugiat in ante metus. Nisl condimentum id venenatis a condimentum vitae sapien pellentesque. A cras semper auctor neque vitae tempus quam. Mauris nunc congue nisi vitae. Donec et odio pellentesque diam volutpat commodo sed egestas egestas. Sed ullamcorper morbi tincidunt ornare massa eget egestas purus. Vulputate ut pharetra sit amet aliquam id diam maecenas ultricies. Viverra orci sagittis eu volutpat odio facilisis mauris sit. Suscipit tellus mauris a diam maecenas sed enim ut. Venenatis cras sed felis eget velit. Tortor pretium viverra suspendisse potenti nullam ac tortor vitae. Scelerisque varius morbi enim nunc faucibus. Sed blandit libero volutpat sed.

# Conclusion

Integer vitae justo eget magna fermentum iaculis eu non. Pulvinar mattis nunc sed blandit libero volutpat sed. Est lorem ipsum dolor sit amet consectetur adipiscing. Vitae suscipit tellus mauris a diam. Volutpat blandit aliquam etiam erat velit scelerisque in dictum. Nibh mauris cursus mattis molestie. Adipiscing elit duis tristique sollicitudin nibh sit amet. Nunc consequat interdum varius sit amet. Eget duis at tellus at urna condimentum mattis pellentesque id. Leo vel orci porta non pulvinar. Adipiscing vitae proin sagittis nisl rhoncus mattis. Felis bibendum ut tristique et egestas. Blandit cursus risus at ultrices mi tempus imperdiet nulla malesuada. Malesuada nunc vel risus commodo viverra maecenas. Vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras. Risus viverra adipiscing at in tellus. Duis ut diam quam nulla porttitor. Sed cras ornare arcu dui vivamus. Sed adipiscing diam donec adipiscing tristique risus. Turpis tincidunt id aliquet risus feugiat in \namecite{Coogan-Gillis-2018}.

