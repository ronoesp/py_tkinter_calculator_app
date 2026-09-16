class SerchingIndex2DArray():
    def __init__(self):
        self.list = []
        
    def set_list(self, new_data_list):
        self.list = new_data_list
        
    #  name数を取得
    def get_list_length(self) -> int:
        return sum(len(row) for row in self.list)
    
    # indexがnames配列の範囲内かチェック
    def is_index_in_range(self, index : int) -> bool:
        if(index < 0):
            return False
        elif(index > self.get_list_length() - 1):
            return False
        else:
            return True
    
    # 指定番号のnameを取得
    def get_data(self, index : int) -> str:
        if( self.is_index_in_range(index) == False ):
            return ""
        
        # 通し番号から「行（row）」と「列（col）」を計算
        row = self.get_index_row(index)  # 商（何行目か）
        col = self.get_index_col(index)  # 余り（何列目か）
    
        # 二次元配列から値を取得して返す
        return self.list[row][col]
    
    def get_index_row(self, index : int) -> int:
        if( self.is_index_in_range(index) == False ):
            return -1
        
        num_columns = len(self.list[0]) # 行数を取得
        row = index // num_columns  # 商（何行目か）
        return row
    
    def get_index_col(self, index : int) -> int:
        if( self.is_index_in_range(index) == False ):
            return -1
        
        num_columns = len(self.list[0]) # 行数を取得
        col = index % num_columns   # 余り（何列目か）
        return col