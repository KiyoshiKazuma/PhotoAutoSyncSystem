<!-- 目次 -->
<a id="Index"></a>
# 目次
- [1 要件](#Req)
    - [1.1 概要](#ReqOverview)
<a id="Req"></a>

# 1.要件

<a id="ReqOverview"></a>
## 1.1.概要
[目次](#Index)
|要件番号|項目|概要|
|:-|:-|:-|
|1|neural network|分岐のないニューラルネットワークを構築できること|
|2|deep-learning|ニューラルネットワークの学習ができること|
|3|save-load|ニューラルネットワークの情報を保存・呼び出しして再利用できること。|
|4|Flex-Initialize|ニューラルネットワークの構成を指定して(Layerの組み換え)初期化が可能であること。|
|5|teacher data file|外部で生成した教師データを読み込んで利用することができること|
|6|learning state|学習進捗を出力することができること。|

<a id="FunctionOverview"></a>

#### Sigmoid
・概要
各要素についてSigmoid活性化関数を作用させ、出力する。
・入出力要素数
$$
\text{inputsize} = \text{outputsize}
$$
・順伝播関数
$$
Y[i]=\frac1 {1+\text{exp}(-X[i])}
$$
・逆伝播関数
$$
\frac{\partial L}{\partial X[i]} =\frac{\partial L}{\partial Y[i]} Y[i](1-Y[i])
$$