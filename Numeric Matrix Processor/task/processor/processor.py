import copy


class Matrix:
    def __init__(self, rows, cols):
        self.rows = int(rows)
        self.cols = int(cols)
        self.matrix_arr = []

        for _ in range(self.rows):
            self.matrix_arr.append([float(n) for n in input().split()])


class MatrixCalculator:
    def __init__(self):
        self.addition_res = None
        self.multiple_const_res = None
        self.multiplication_res = []

    def start(self):
        while True:
            op_num = self.get_user_choice()
            if op_num == 1:
                m_1, m_2 = self.read_two_matrices()
                self.add_matrices(m_1, m_2)
            elif op_num == 2:
                mx, num = self.read_const_matrix()
                self.multiply_const(mx, num)
            elif op_num == 3:
                m_1, m_2 = self.read_two_matrices()
                self.multiply_matrices(m_1, m_2)
            elif op_num == 4:
                user_choice = self.user_trans_choice()
                mx = self.read_trans_matrix()
                self.trans_matrix(user_choice, mx)
            elif op_num == 5:
                mx = self.read_trans_matrix()
                determinant = self.calculate_determinant(mx.matrix_arr, 1)
                print("The result is:")
                print(determinant)
            elif op_num == 6:
                mx = self.read_trans_matrix()
                self.find_inverse(mx)
            elif op_num == 0:
                break

    def find_inverse(self, mx):
        determinant = self.calculate_determinant(mx.matrix_arr, 1)
        if determinant == 0:
            print("This matrix doesn't have an inverse.")
        else:
            transposed_mx = []
            for m_row in range(mx.rows):
                arr = []
                for m_col in range(mx.cols):
                    arr.append(mx.matrix_arr[m_col][m_row])
                transposed_mx.append(arr)

            connected_matrix = [row[:] for row in transposed_mx]
            for i in range(len(connected_matrix[0])):
                for j in range(len(connected_matrix[0])):
                    min_mx = self.get_cofactor(transposed_mx, i, j)
                    min_mx = [
                        [min_mx[i][j] for j in range(len(min_mx[0]))]
                        for i in range(len(min_mx))
                    ]
                    connected_matrix[i][j] = (-1)**(i + j) * self.calculate_determinant(min_mx, 1)

            scalar = 1 / determinant

            res_mx = [
                [int(connected_matrix[i][j] * scalar * 100) / 100
                 if connected_matrix[i][j] != 0
                 else 0 for j in range(len(connected_matrix[0]))]
                for i in range(len(connected_matrix))
            ]

            print("The result is:")
            for a in res_mx:
                print(*a)

    @staticmethod
    def get_cofactor(m, i, j):
        m_copy = copy.deepcopy(m)
        del m_copy[i]
        for i in range(len(m[0]) - 1):
            del m_copy[i][j]
        return m_copy

    def calculate_determinant(self, mx, mul):
        width = len(mx)
        if width == 1:
            return mul * mx[0][0]
        else:
            sign = -1
            total = 0
            for i in range(width):
                m = []
                for j in range(1, width):
                    buff = []
                    for k in range(width):
                        if k != i:
                            buff.append(mx[j][k])
                    m.append(buff)
                sign *= -1
                total += mul * self.calculate_determinant(m, sign * mx[0][i])
            return total

    def multiply_matrices(self, m_1, m_2):
        if m_1.cols != m_2.rows:
            self.operation_error()
        else:
            arr = []
            for i in range(m_1.rows):
                for row_i in range(m_2.cols):
                    total = 0
                    for col_i in range(m_1.cols):
                        total += m_1.matrix_arr[i][col_i] * m_2.matrix_arr[col_i][row_i]
                    arr.append(total)
                self.multiplication_res.append(arr)
                arr = []
        self.print_res('multiplication')

    def add_matrices(self, m_1, m_2):
        if m_1.rows == m_2.rows and m_1.cols == m_2.cols:
            self.addition_res = [
                [m_1.matrix_arr[i][j] + m_2.matrix_arr[i][j] for j in range(m_1.cols)]
                for i in range(len(m_1.matrix_arr))
            ]
            self.print_res('addition')
        else:
            self.operation_error()

    def multiply_const(self, m, scalar):
        self.multiple_const_res = [
            [m.matrix_arr[i][j] * scalar for j in range(m.cols)]
            for i in range(len(m.matrix_arr))
        ]
        self.print_res('multiply_const')

    @staticmethod
    def trans_matrix(option, mx):
        res_mx = []
        if option == 1:
            for m_row in range(mx.rows):
                arr = []
                for m_col in range(mx.cols):
                    arr.append(mx.matrix_arr[m_col][m_row])
                res_mx.append(arr)
        elif option == 2:
            for m_col in range(mx.cols - 1, -1, -1):
                arr = []
                for m_row in range(mx.rows - 1, -1, -1):
                    arr.append(mx.matrix_arr[m_row][m_col])
                res_mx.append(arr)
        elif option == 3:
            for m_row in range(mx.rows):
                arr = []
                for m_col in range(mx.cols - 1, -1, -1):
                    arr.append(mx.matrix_arr[m_row][m_col])
                res_mx.append(arr)
        elif option == 4:
            for m_row in range(mx.rows - 1, -1, -1):
                arr = []
                for m_col in range(mx.cols):
                    arr.append(mx.matrix_arr[m_row][m_col])
                res_mx.append(arr)

        print('The result is:')
        for a in res_mx:
            print(*a)

    def print_res(self, action):
        print('The result is:')
        if action == 'addition':
            for a in self.addition_res:
                print(*a)
                self.addition_res = None
        elif action == 'multiply_const':
            for a in self.multiple_const_res:
                print(*a)
                self.multiple_const_res = None
        elif action == 'multiplication':
            for a in self.multiplication_res:
                print(*a)
                self.multiplication_res = []
        print('\n')

    @staticmethod
    def read_two_matrices():
        rows_1, cols_1 = input('Enter size of first matrix:').split()
        print('Enter first matrix:')
        m_1 = Matrix(rows_1, cols_1)
        rows_2, cols_2 = input('Enter size of second matrix:').split()
        print('Enter second matrix:')
        m_2 = Matrix(rows_2, cols_2)
        return [m_1, m_2]

    @staticmethod
    def read_const_matrix():
        m_rows, m_cols = input('Enter size of matrix:').split()
        print('Enter matrix:')
        mx = Matrix(m_rows, m_cols)
        num = int(input('Enter constant:'))
        return [mx, num]

    @staticmethod
    def read_trans_matrix():
        m_rows, m_cols = input('Enter matrix size:').split()
        print('Enter matrix:')
        mx = Matrix(m_rows, m_cols)
        return mx

    @staticmethod
    def user_trans_choice():
        print("1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        user_choice = int(input("Your choice"))
        return user_choice

    @staticmethod
    def get_user_choice():
        print("1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("0. Exit")
        user_choice = int(input())
        print(f"Your choice: > {user_choice}")
        return user_choice

    @staticmethod
    def operation_error():
        print('The operation cannot be performed.')


MatrixCalculator().start()
