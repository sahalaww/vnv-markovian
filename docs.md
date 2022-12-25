# Docs Markovian Approximation

## Formula Dasar

![eq-1](https://quicklatex.com/cache3/80/ql_b0fce36a5db273466faf0cf7c3837680_l3.png)

Lalu kami ingin melakukan perhitungan melalui pendekatan dengan formula 

![](https://quicklatex.com/cache3/fb/ql_2acee0a804f1596f1de8813bb0ef6bfb_l3.png)

yang mana nilai tersebut merupakan transient probability $Π(t)_{(s,0)(s',j)}^{C{\infty}}$ ketika di suatu state $(s',j)$ di waktu $t$ yang telah dimulai pada saat state $(s, 0)$ 

Nilai matriks $\bold{Q}^{\infty}$ dibentuk dari matriks $\bold {Q}$ dan $\bold {D}$.  Nilai matriks $\bold{Q}$ dihitung dari $\bold {R}$ (rate matrix/transisi matriks ke tiap state) dan matriks $\bold {D}$ dengan nilai diagonal utamanya dari vektor reward $\rho$.

Berikut formula untuk menghitung nilai matriks generator $\bold {Q}$:

$$ Q_{ss'} = \left\{ 
  \begin{array}{ c l }
    R_{ss'}                 & \quad {s \neq s'} \\
    -\sum_{z\neq s} R_{ss'} & \quad {s = s'}
  \end{array}
\right. $$

Selanjutnya, untuk matriks $\bold {D}$ dapat dibentuk dari vektor reward ($\rho$), 

$$ D = diag(\rho) $$

Perhitungan $Π(t)$ secara efektif dapat dilakukan dengan uniformisation karena pada formula


$$ Π(t) = Π(0) . e^{Qt} = \sum_{n=0}^{\infty} \frac{(Qt)^n}{n!}  \quad  \textrm{, dimana nilai } { Π(0) = {\bold {I}}} $$

Komputasi matrix exponential untuk $\bold Q$ tidak feasible. Maka, dapat didefinisikan matrix $\bold U$ (stochastic matrix)

$$ \bold {U} = \bold {I} + \frac{1}{\lambda} \bold {Q} \quad \rightarrow \quad \bold {Q} = \lambda(\bold {U} - \bold {I}) \quad , \lambda = max(diag(\bold {Q}))$$

Sehingga,

$$ \begin{split}
    Π(t) & = e^{\lambda( \bold {U} - \bold {I})t} \\
         & = e^{-\lambda t} . e^{\lambda t \bold {U}} \\
        & = \sum_{z\neq s}^{\infty}  e^{-\lambda t} \frac{(\lambda t)^n}{n!} . \bold {U}^n \quad , \textrm { nilai } \bold {U}^0 = \bold {I}, \bold {U}^n = \bold {U}^{n-1}. \bold {U}
\end{split}$$

Pada formula diatas, nilai $e^{-\lambda t} \frac{(\lambda t)^n}{n!} $ adalah $PP $ atau poisson probability. 

Maka menjadi,

$$
    Π(t) = \sum_{n=0}^{N} PP(-\lambda t, n). \bold {U}^n
$$

Agar perhitungan tidak sampai nilai $N$, maka dapat menggunakan error bound yang dihitung secara apriori melalui:

$$
\varepsilon = 1 - \sum_{n=0}^{N} PP(-\lambda t, n)
$$


## Implementasi Algoritme dan Contoh Perhitungan

Contoh kasus pada gambar diambil dari [1]. 
![Four state mrm](/images/four-state-mrm.png)

Terdapat 4 state dan 6 transisi, dengan nilai reward $\rho = (50, 20, 100, 0)$. Initial distribution yang ditetapkan adalah $\alpha = (1, 0, 0, 0)$ , lalu nilai $t=0.2$ dan $y=5$


Untuk melakukan perhitungan joint distribution dengan menggunakan markovian approximation dapat dilakukan dengan step berikut:

1. Mendefinisikan rate matriks $\bold {R}$ pada `.tra` file

```
STATES 4
TRANSITIONS 6
1 2 3
1 3 6
1 4 1
2 1 2
3 1 8
4 1 1
```

2. Mendefinisikan initial distribution pada `.pi` file

```
1 1
```

3. Mendefinisikan reward rate pada `.rew` file

```
1 50
2 20
3 100
```

4. Menjalankan simulasi berdasarkan parameter diatas dengan memanggil file `main.py`

```
python main.py -t samples/game.tra -r samples/game.rew -p samples2/game.pi -d 0.1 -tm 0.2 -ym 5 -e 0.01 -o sample-out.txt
```

-t  merupakan argument untuk memasukan nilai path file `.tra` 

-r  merupakan argument untuk memasukan nilai path file `.rew` 

-p  merupakan argument untuk memasukan nilai path file `.rew` 

-d merupakan argument untuk memasukan nilai `delta`

-tm merupakan argument untuk memasukan nilai `t_max`

-ym merupakan argument untuk memasukan nilai `y_max`

-e  merupakan argument untuk memasukan nilai `epsilon`

-o  merupakan argument untuk memasukan path output file yg akan menyimpan hasil transient distribution


5. Program akan membaca  `.tra`, `.rew` dan `.pi` file, lalu meneruskan argument lain seperti `delta`, `t_max` , `y_max` dan `epsilon` untuk inisiasi class `MarkovianApproximation`. Kemudian memanggil fungsi `compute_joint_distribution` untuk mendapatkan nilai $\Upsilon$. 


## Hasil

Hasil yang diperoleh dari simulasi diatas dengan $\varepsilon = 0.01$

| $\Delta y$      | $Pr \{{ Y_{0.2} \leq 5 }\} $ | Time (s)    |
| --------------- | -------------------------------- |------------ |
| $10^{-1}$       | 0.12157013167794681              | 0.4         |


Benchmark dengan hasil pada paper, nilai $\varepsilon = 10^-16$


| $\Delta y$      | $Pr\{{ Y_{0.2} \leq 5 }\} $ | Time (s)    |
| --------------- | -------------------------------- |------------ |
| $10^{-1}$       | 0.1294067747                     | 0.003       |
| $10^{-2}$       | 0.1324884190                     | 0.232       |
| $10^{-3}$       | 0.1329690459                     | 20.56       |


## References

[1] L. Cloth, B.R. Haverkort, Five Performability Algorithms: A Comparison, in: MAM 2006: Markov Anniversary Meeting, Boson Books, 2006: pp. 39–54. https://research.utwente.nl/en/publications/five-performability-algorithms-a-comparison (accessed September 10, 2022).
