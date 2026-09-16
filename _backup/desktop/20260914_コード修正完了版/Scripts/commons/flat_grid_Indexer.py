class FlatGridIndexer():
    """1次元配列(フラットな配列)を、行×列の格子(グリッド)として扱うためのクラス。

    実体はフラットな1次元配列だが、列数(num_columns)を指定することで、
    通し番号(index)と行・列を相互に変換しながらアクセスできるようにする。

    全ての行の要素数が同じ「長方形」の格子であることを前提とする。
    """

    def __init__(self):
        self.list = []
        self._num_columns = 0

    def set_list(self, flat_list, num_columns: int):
        """フラットな1次元配列と、1行あたりの要素数(列数)を設定する。

        flat_list の要素数が num_columns で割り切れることを前提とする
        （長方形の2次元配列をフラット化したものを想定）。
        """
        self.list = flat_list
        self._num_columns = num_columns

    # 要素数を取得
    def get_list_length(self) -> int:
        return len(self.list)

    # indexが配列の範囲内かチェック
    def is_index_in_range(self, index: int) -> bool:
        return 0 <= index < self.get_list_length()

    # 指定番号の要素を取得
    def get_data(self, index: int) -> str:
        if not self.is_index_in_range(index):
            return ""
        # フラット配列なので、行・列に変換せずそのままアクセスできる
        return self.list[index]

    def get_index_row(self, index: int) -> int:
        if not self.is_index_in_range(index):
            return -1
        return index // self._num_columns

    def get_index_col(self, index: int) -> int:
        if not self.is_index_in_range(index):
            return -1
        return index % self._num_columns
