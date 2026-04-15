# Pyxel アナログ時計 仕様書

## 概要

Python の retro ゲームエンジン [Pyxel](https://github.com/kitao/pyxel) を使ったアナログ時計アプリ。

## 起動方法

```bash
pip install pyxel   # 未インストールの場合
python main.py
```

- **Q キー** で終了

## ファイル構成

```
pyxel_clock/
├── main.py    # エントリポイント。clock.run() を呼び出す
├── clock.py   # App クラス定義、pyxel の初期化・ループ管理
├── face.py    # 文字盤描画（ベゼル、目盛り）
├── hands.py   # 針描画（時針・分針・秒針）
└── utils.py   # 座標変換ヘルパー
```

## 技術仕様

| 項目             | 値                        |
|------------------|---------------------------|
| 画面サイズ       | 128×128 px                |
| 表示スケール     | 4 (→ 512×512 ウィンドウ)  |
| 中心座標         | cx=64, cy=64              |
| 時計半径         | 58 px                     |
| FPS              | 30                        |
| Python バージョン | 3.x                       |
| Pyxel バージョン | 2.x (display_scale 対応)  |

## モジュール詳細

### `main.py`

エントリポイント。`clock.run()` を呼び出すだけ。

### `clock.py`

- `App` クラス: `pyxel.init` → `pyxel.run` でループ開始
- `update()`: Q キー入力で `pyxel.quit()`
- `draw()`: 毎フレーム `datetime.datetime.now()` を取得し、`draw_face` → `draw_hands` → デジタル時刻テキストの順で描画
- `run()`: `App()` をインスタンス化する関数（`main.py` から呼ばれる）

### `face.py`

`draw_face(cx, cy, radius)`:

1. `pyxel.circ(cx, cy, radius, 1)` — 濃紺の文字盤塗りつぶし
2. `pyxel.circb(cx, cy, radius, 2)` — 外ベゼル
3. `pyxel.circb(cx, cy, radius-1, 6)` — 内ベゼル
4. 時間目盛り 12本: `fraction = i/12`、`radius-3` → `radius-7` の線、色 6
5. 分目盛り 60本: `fraction = i/60`、5の倍数はスキップ、`radius-2` → `radius-4` の線、色 13
6. 中心ピボット: `pyxel.circ(cx, cy, 2, 11)`

### `hands.py`

`draw_hands(cx, cy, h, m, s)`:

**フラクション計算（スムーズな動き）:**
```python
sec_fraction  = s / 60
min_fraction  = (m + s / 60) / 60
hour_fraction = ((h % 12) + m / 60) / 12
```

**針の仕様:**

| 針   | 先端半径 | 尾半径 | 色  | 太さ処理               |
|------|---------|--------|-----|------------------------|
| 時針 | 32 px   | -8 px  | 7   | cx+1 にオフセット線を追加 |
| 分針 | 48 px   | -10 px | 7   | cx+1 にオフセット線を追加 |
| 秒針 | 52 px   | -14 px | 8   | 1px のみ               |

描画順: 時針 → 分針 → 秒針（秒針が最前面）

### `utils.py`

```python
def angle_to_xy(cx, cy, radius, fraction):
    """
    fraction: 0.0=12時, 0.5=6時 (時計回り)
    戻り値は必ず int (Pyxel の描画関数に float を渡すと TypeError)
    """
```

## カラーパレット（Pyxel デフォルト）

| Index | 色       | 用途                       |
|-------|----------|----------------------------|
| 0     | 黒       | 背景                       |
| 1     | 濃紺     | 文字盤背景                 |
| 2     | 暗紫     | 外ベゼル                   |
| 6     | 薄グレー | 内ベゼル・時間目盛り       |
| 7     | 白       | 時針・分針・デジタル表示   |
| 8     | 赤       | 秒針                       |
| 11    | 水色     | 中心ピボット               |
| 13    | ピーチ   | 分目盛り                   |

## 注意点

- `angle_to_xy` の戻り値は `int(round(...))` で整数化している
- `datetime.now()` は `draw()` 内で毎フレーム呼ぶ（`update()` ではなく `draw()` で取得）
- `display_scale` は Pyxel 2.x から対応
