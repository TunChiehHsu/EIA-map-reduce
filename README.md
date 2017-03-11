# EIA_single_machine

###Introduction

A directed cycle means that
a directed path consists of a sequence of vertices starting and ending at the same vertex.
In a trading network,
a directed cycle means members of a cycle construct a closed trading system,
which would possibly contain some abnormal trading manners.
In general,
we are interested in detecting these cycles with different length.
In the following paragraphs,
we will use the $k$-length cycle or $C_k$ to represent the cycles with length $k$.
It should be noted that the choice of starting vertex is not important
since traversing the same cyclic sequence of edges from different starting vertices produces the same closed walk,
i.e., \textit{repeated cycles}.

###Problems in Traditional Cycle detection
There are several problems in the literature of traditional cycle detection.
One of the major topics is the detection of ``inner cycle''.
Suppose a path with length $k$ is denoted as $k$-length path or $P_{k}$ in abbreviation.
An inner cycle is defined as an cycle $C^{\iota}_{d}$ which is included in $P_{k}$ where $d < k$.
From Fig.\ref{inner}(a), we can observe that a 3-length cycle
$C \rightarrow D \rightarrow E \rightarrow C$ was included in a
$P_{6} = A \rightarrow B \rightarrow C \rightarrow D \rightarrow E \rightarrow C \rightarrow F$
Traditional method utilizing matrix computing or other detection algorithm did not take inner cycle into consideration.
The extension or application based on these inner cycles may result in a waste of memory and produce additional computational burden.

The other problem is ``repeated cycle''.
A cycle might be recorded repeatedly since that each cycle could be represented in different ways by selecting different nodes as the ``head''.
Consider a $k$-length cycle $C_{k} = (v_{1} \rightarrow v_{2} \rightarrow ... \rightarrow v_{k} \rightarrow v_{1})$.
Define the node set $V_c = \{v_{1},v_{2},...,v_{k}\}$.
$C_{k}$ could be represented as a cycle started from any nodes in set $V_c$.
That is, $C_{k}$ can be represented as $(v_{2} \rightarrow v_{3} \rightarrow ... \rightarrow v_{k} \rightarrow v_{1} \rightarrow v_{2})$.
In general, a $k$-length cycle $C_{k}$ has $k$ different representations.
We take a 4-length cycle $C_{4}$ for an example, and the structure of the $C_4$ is presented in Fig.\ref{inner}(b).
Different representations was classified in Table \ref{repcyctable}.
The deletion of repeated cycle could reduce great amount of memory and improve computing efficiency.

\begin{table}[!h]
\centering
\caption{Different Representations of $C_{4}$ in Fig.\ref{repeat}(b)} \label{repcyctable}
\label{repeat}
\begin{tabular}{l}
A $\rightarrow$ B $\rightarrow$ C $\rightarrow$ D $\rightarrow$ A \\
B $\rightarrow$ C $\rightarrow$ D $\rightarrow$ A $\rightarrow$ B \\
C $\rightarrow$ D $\rightarrow$ A $\rightarrow$ B $\rightarrow$ C \\
D $\rightarrow$ A $\rightarrow$ B $\rightarrow$ C $\rightarrow$ A
\end{tabular}
\end{table}

\section{Preliminary for Data Preprocessing}

While analyzing a large scale network,
redundant data might slow down the computational speed and increase the computing burden.
Thus, we have to process the data before applying the algorithm.

\subsection{Remove the isolate nodes}

In the first step of data preprocessing,
we have to delete the isolate nodes among the directed network.
The node could be a head of a cycle only when it is both a receiver and deliver simultaneously.
As a result, we selected this nodes to keep in the directed network and deleted others.
In our experience, when the connecting probability is 80\%,
the amount of the nodes in the directed network could be reduced by 10\% to 15\%.
We take the trading network in Fig.\ref{remove} for an example.
The red nodes should be removed due to they are not both a seller and buyer.

\begin{figure}[!h]
    \centering
    \includegraphics[trim = 1cm 5cm 1cm 4cm,clip =TRUE,width=0.4\textwidth]{plot/remove.eps}
    \caption{Removing the isolate points from directed network}\label{remove}
    \end{figure}

\subsection{Strongly Connected Component}

In the mathematical theory of directed graphs,
a graph is said to be strongly connected if every vertex is reachable from every other vertex.
The strongly connected components of an arbitrary directed graph form a partition into subgraphs
that are themselves strongly connected.
It is possible to test the strong connectivity of a graph, or to find its strongly connected components, in linear time.

%write the form of algorithm
Call two nodes $u$ and $v$ of a directed graph $G = (V;E)$ connected if there is a path from $u$ to $v$,
and one from $v$ to $u$. As such, it partitions $V$ into disjoint sets,
called the strongly connected components of the graph.
If we shrink each of these strongly connected components down to a single node,
and draw an edge between two of them if there is an edge from some node in the first to some node in the second,
the resulting directed graph has to be a directed acyclic graph (dag in abbreviation),
that is to say, it can have no cycles.
The reason is simple:
A cycle containing several strongly connected components would merge them all to a single strongly connected component.
We can restate this observation as follows: Every directed graph is a dag of its strongly connected components.
From the Fig.\ref{strong}, the network could be split into two parts.

\begin{figure}[!h]
    \centering
    \includegraphics[trim = 1cm 5cm 1cm 4cm,clip =TRUE,width=0.4\textwidth]{plot/strong.eps}
    \caption{Split the network by strongly connected component}\label{strong}
    \end{figure}

\section{Methodology}

\subsection{Endpoint Inward Algorithm (EIA)}
We defined a directed labeled graph as $G = (V, E)$,
where $V$ is the set of vertices with ordered labele $V = \{v_1,v_2,\ldots,v_n\}$
and $E$ is the set of directed edges  $E=\{e_1,e_2,\ldots,e_m\}$.

%\leftline{\textbf{Definition}}
In general, this algorithm contains three types of sets.
The first one is the set of cycle with length $k$, defined as $C_{k}$.
Another is the set of ``ascending order path" with distance $k$ which is defined as $P_k(A)$.
$P_k(A)$ contains paths $p_k(A)$ where the labels of the leaders are smaller than those of the end.
The other is the set of ``descending order path" with length $k$ which is defined as  $P_{k}(D)$.
$P_k(D)$ contains paths $p_k(D)$ where in the labels of the leaders are larger than those of the end. \\

%\leftline{\textbf{Definition}}
In addition, two major operators were used to operate two different paths;
the first one is the ``merge" operator $\bigotimes$ which is used to construct a new path
when one path's head and end is same as the end and head of another path, respectively.
Another operator is the ``extend" operator $\bigoplus$
which is used to build a path if one path's end is the head of another path.
How these two operators work were illustrated in the following example.
Suppose there are three paths,
$p_1=(D \rightarrow C),p_2=(D \rightarrow E \rightarrow A),p_3=(A \rightarrow B \rightarrow D)$.
\begin{equation*}
    \begin{split}
    p_3 \bigotimes p_2 &= (A \rightarrow B \rightarrow D \rightarrow E \rightarrow A) \mbox{,which is a length 4 cycle}\\
    p_3 \bigoplus p_1 &= (A \rightarrow B \rightarrow D \rightarrow C) \mbox{,which is an extended length 3 path.}\\
    \end{split}
\end{equation*}

\begin{algorithm}
    \caption{EIA algorithm}
    \begin{algorithmic}
        \Procedure{EIA}{$G=(V, E)$}
        \State Initially group the edge set $E$ into two disjointed sets $P_1(A)$ and $P_1(D)$,
        and $E=P_1(A) \bigcup P_1(D)$.
        \State In general, this algorithm contains three phases with each given distance.
        \For{$k$ = 1 to $K$}
        \State  I. \underline{Find Cycles by $k \bigotimes k$}: \newline
        Detect all length possible $2k$ cycles by $P_k(A) \bigotimes P_k(D)$.\\
        \State  II. \underline{Extend Paths of $P_k(A)$ and Find Cycles by $k+1 \bigotimes k$}: \newline
        Extend paths by $P_{k+1}(A) = P_k(A) \bigoplus E$. \newline
        Detect all length possible $2k+1$ cycles by $P_{k+1}(A) \bigotimes P_k(D)$.
        \State  III. \underline{Extend Paths of Descending Order Path Set}: \newline
        Extend paths by $P_{k+1}(D) = P_k(D) \bigoplus E$.\\
        \EndFor
        \State \textbf{return} The set of cycles $C$.\\
        \Comment{After running $K$ times, we can get all possible cycles with lengths from 2 to $2K+1$.}
        \EndProcedure
    \end{algorithmic}
\end{algorithm}

\subsection{Toy Example}

We now introduced the algorithm with an application on the simulated network $G$ (Figure \ref{sim}).
Notice that $G$ could contain parallel edges in opposite directions but cannot have self-loops.
Also, isolated vertices mentioned in last chapter should be removed from the graph
due to it is impossible for them to become a member of cycle.
A simulated graph $G$ with 4 vertices and 7 edges was shown in Figure\ref{sim}.

\begin{figure}[!h]
    \centering
    \includegraphics[trim = 1cm 5cm 1cm 4cm,clip =TRUE,width=0.4\textwidth]{plot/simulation.eps}
    \caption{The simulation network $G$}\label{sim}
\end{figure}

All edges $E$ are were shown in Table \ref{simulationg} and was classified to $P_1(D)$ and $P_1(A)$.
The algorithm first apply $P_1(A)$ $\bigotimes$ $P_1(D)$
and then $C_2 = (C \rightarrow D \rightarrow C)$ was generated.

\rowcolors{2}{gray!25}{white}
\begin{table}[!h]
\centering
\caption{All edges $E$ of the simulated network $G$} \label{simulationg}
\begin{tabular}{C{2cm}C{2cm}C{2cm}}
\rowcolor{gray!50}
Head &  & End \\
A & $\rightarrow$ & C  \\
B & $\rightarrow$ & A  \\
B & $\rightarrow$ & D  \\
C & $\rightarrow$ & B  \\
C & $\rightarrow$ & D  \\
D & $\rightarrow$ & A  \\
D & $\rightarrow$ & C
\end{tabular}
\end{table}

Next, we extend the path $P_1(A)$ to length 2 by operating $p_1(A) \bigoplus E$ and obtain
$P_2(A) = {\{(A \rightarrow C \rightarrow B),(A \rightarrow C \rightarrow D)\}}$.
Notice that each $p_k(A)$ could be contained in $P_k(A)$ only when its end is larger then head.
Also, the paths containing inner cycles should be removed as well.
After obtaining $P_2(A)$, we apply the $\bigotimes$ for length 2 cycle set.
Thusly, $C_3$ could be generated from $P_2(A) \bigotimes P_1(D)$
where $C_2 = {\{(A \rightarrow C \rightarrow B \rightarrow A),(A \rightarrow C \rightarrow D \rightarrow A)\}}$.
During the operation, inner cycles should also be eliminated.

We now extend the descending order path $P_1(D)$ to length 2.
In this step $P_2(D) = \{(C \rightarrow B \rightarrow A),(C \rightarrow D \rightarrow A),(B \rightarrow D \rightarrow A) \}$
was generated from $E \bigoplus p_1(D)$.
Due to $P_2(D)$ should follows descending order,
the head of the every path $p_2(D)$ in $P_2(D)$ should be larger than the end.
Otherwise, it should be eliminated.
Also, inner cycles should be removed from the set in this step.

Further, we take $P_2(D) and P_2(A)$ as input and start from step I again to obtain $C_4, P_3(I), C_5,$ and $P_3(D)$.
The iteration continues until our reaching our selected length cycles or one of the set  $P_k(A)$ or $P_k(D)$ is a null set.

\subsection{Expected Storage Burden of Paths and Cycles}
In this section,
we study the expected computing burden of finding cycles.
Generally speaking,
suppose we deal with a random graph with $n$ vertices and a common connection probability $p$.
The expected number of a $k$-length path is easily evaluated by the binomial distribution.
Given a node $v_i$ as the started point of a path,
the number of neighbors follows a binomial distribution $Binom(n,p)$.
If we consider the paths without inner cycles,
we can evaluate the number of $k$-length paths started from $v_i$ by
\begin{equation}
  E(p_i (k)) = \Pi_{d=1}^k (n-d)p.
\end{equation}
Since we assume all nodes with the same connection probability,
the total number of $k$-length paths is
\begin{equation}
  E(P (k)) = n \times \{\Pi_{d=1}^k (n-d)p\},
\end{equation}
and the total number of $(k+1)$-length cycles is
\begin{equation}
  E(C (k+1)) = n \times \{\Pi_{d=1}^k (n-d)p\} \times p.
\end{equation}

Our empirical data is collected from 1,385,870 companies and 113,244,475 trades,
that is, connection probability $p=5.896e-05$.
Based on the above equations,
we summarize the expected numbers of paths and cycles.
In addition, we also list the expected storage sizes for saving these data sets in the following table
(suppose we are only interested in $C_7$).

\begin{table}[ht]
\footnotesize
\centering
\caption{Expected storage sizes for saving paths and cycles with $n=1,385,870$ and $p=5.896e-05$.}
\begin{tabular}{lrrrrrrr}
  \toprule
Length & 1 & 2 & 3 & 4 & 5 & 6 & 7\\
  \midrule
\parbox[c]{2cm}{Expected \# of Paths} & 1.13e+08 & 9.25e+09 & 7.56e+11 & 6.18e+13 & 5.05e+15 & 4.13e+17 & \\
\parbox[c]{2cm}{Expected \# of Cycles} & & 6.68e+03 & 5.46e+05 & 4.46e+07 & 3.64e+09 & 2.98e+11 & 2.43e+13 \\
\parbox[c]{2cm}{Expected Stored Size of Paths (MB)} & 3.32e+05 & 3.62e+07 & 3.69e+09 & 3.62e+11 & 3.45e+13 & 3.22e+15 & \\
\parbox[c]{2cm}{Expected Stored Size of Cycles (MB)} & & 2.61e+01 & 2.66e+03 & 2.61e+05 & 2.49e+07 & 2.33e+09 & 2.14e+11 \\
   \bottomrule
\end{tabular}
\end{table}

Obviously, it is not possible for a personal computer to execute such a big data analysis according to above results
(3001653 petabytes for saving 6-length paths).
Even for a large cluster platform,
it is also not a workable case.
For this reason,
we use a smaller case to show that the EIA is a useful algorithm to save the storage sizes.
In the following simulation case,
we generate a network with $n=10,000$ and $p=0.001$, i.e., each node expectedly has 10 neighbors.

\begin{table}[ht]
\footnotesize
\centering
\caption{Expected storage sizes for saving paths and cycles with $n=1,385,870$ and $p=5.896e-05$.}
\begin{tabular}{lrrrrrrr}
  \toprule
Length & 1 & 2 & 3 & 4 & 5 & 6 & 7\\
\midrule
  \parbox[c]{2cm}{Expected \# of Paths} & 1e+05 & 1e+06 & 9.99e+06 & 9.99e+07 & 9.99e+08 & 9.98e+09 &\\
  \parbox[c]{2cm}{Simulated \# of Paths} & 99800 & 6.65e+05 & 4.98e+06 & 1.96e+07 &  &  &\\
  \parbox[c]{2cm}{Expected \# of Cycles} & & 100 & 1000 & 9990 & 9.99e+04 & 9.99e+05 & 9.98e+06 \\
 \parbox[c]{2cm}{Simulated \# of Cycles} & & 48 & 348 & 2553 & 20290 & 1e+05 & 1.42e+06 \\
  \parbox[c]{2cm}{Expected Stored Size of Paths (MB)} & 1.77 & 25.32 & 329.40 & 4055 & 48150 & 557300 &\\
  \parbox[c]{2cm}{Simulated Stored Size of Paths (MB)} & 1.03 & 7.62 & 76.10 & 375.50 &  &  &\\
  \parbox[c]{2cm}{Expected Stored Size of Cycles (MB)} & & 0 & 0.03 & 0.41 & 4.82 & 55.80 & 633 \\
  \parbox[c]{2cm}{Simulated Stored Size of Cycles (MB)} & & 0 & 0.01 & 0.05 & 0.46 & 4.43 & 43.40 \\
   \bottomrule