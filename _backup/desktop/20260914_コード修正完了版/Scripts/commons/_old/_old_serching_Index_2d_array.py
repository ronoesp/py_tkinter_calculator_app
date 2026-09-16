class SerchingIndex2DArray():
    """2次元配列(二重リスト)を、1次元の通し番号(index)でアクセスするためのクラス。

    全ての行の要素数が同じ「長方形」の2次元配列であることを前提とする。
    行によって要素数が異なる配列（ジャグ配列）を渡した場合の動作は保証しない。
    """

    def __init__(self):
        self.list = []
        self._num_rows = 0
        self._num_columns = 0

    def set_list(self, new_data_list):
        self.list = new_data_list

        # 行数・列数はここで1回だけ計算してキャッシュしておく
        # （呼び出しのたびに全行を走査するのを避けるため）
        self._num_rows = len(new_data_list)
        self._num_columns = len(new_data_list[0]) if self._num_rows > 0 else 0

    # name数を取得
    def get_list_length(self) -> int:
        return self._num_rows * self._num_columns

    # indexがnames配列の範囲内かチェック
    def is_index_in_range(self, index: int) -> bool:
        return 0 <= index < self.get_list_length()

    # 指定番号のnameを取得
    def get_data(self, index: int) -> str:
        if not self.is_index_in_range(index):
            return ""

        row, col = self._to_row_col(index)
        return self.list[row][col]

    def get_index_row(self, index: int) -> int:
        if not self.is_index_in_range(index):
            return -1
        return self._to_row_col(index)[0]

    def get_index_col(self, index: int) -> int:
        if not self.is_index_in_range(index):
            return -1
        return self._to_row_col(index)[1]

    # 通し番号(index)を「行, 列」に変換する（内部専用）
    def _to_row_col(self, index: int):
        return divmod(index, self._num_columns)
