import csv
import operator


class Markov:
    markov_matrix = {}
    his_count = 1
    pre_count = 3
    test_count = 3
    tol = 3

    def __init__(self, his_count=1, pre_count=3, test_count=3, tol=3):
        """
        :param his_count: history point(s) count.
        :param pre_count: prediction point(s) count.
        :param test_count: point(s) count remain for test.
        :param tol: int, tolerant point(s) count of prediction.
        """
        self.his_count = his_count
        self.pre_count = pre_count
        self.test_count = test_count
        self.tol = tol

    def get_predict(self, his_seq: tuple):
        """
        Get prediction from a history sequence.

        :param his_seq: tuple, history sequence.
        :return: list, containing count of tolerant point(s) as a prediction set.
        """
        result = []
        predict_list = self.markov_matrix[his_seq]
        for i in range(self.pre_count):
            pre_i_dict = predict_list[i]
            sorted_i_list = sorted(pre_i_dict.items(), key=operator.itemgetter(1))
            sorted_i_list.reverse()
            result_i = []
            for j in range(self.tol):
                try:
                    result_i.append(sorted_i_list[j][0])
                except IndexError:
                    break
            result.append(result_i)
        return result

    def read_csv(self, file_dir: str):
        """
        Read sequences from one csv file.

        :param file_dir: str, file directory of the csv file.
        """
        with open(file_dir, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.add_row(row)

    def add_row(self, row: list):
        """
        Add one rows to markov matrix.

        :param row: list, containing one row of training sequence.
        """
        input_row = row[:-self.test_count]
        for i in range(len(input_row) - (self.his_count + self.pre_count) + 1):
            his_seq = tuple(input_row[i:i + self.his_count])
            pre_seq = tuple(input_row[i + self.his_count:i + self.his_count + self.pre_count])
            self.add_seq(his_seq, pre_seq)

    def add_seq(self, his_seq: tuple, pre_seq: tuple):
        """
        Add a new sequence to markov matrix.

        :param his_seq: tuple, containing one history sequence.
        :param pre_seq: tuple, containing one prediction sequence.
        """
        try:
            history_row = self.markov_matrix[his_seq]

            for i in range(self.pre_count):
                try:
                    predict_i_count = history_row[i][pre_seq[i]]
                    self.markov_matrix[his_seq][i][pre_seq[i]] = predict_i_count + 1
                except KeyError:
                    self.markov_matrix[his_seq][i][pre_seq[i]] = 1
        except KeyError:
            self.markov_matrix[his_seq] = []
            for point in pre_seq:
                self.markov_matrix[his_seq].append({point: 1})

    def test_seq(self, his_seq: tuple, real_seq: tuple):
        """
        Use current markov matrix to run a test and return accuracy.

        :param his_seq: tuple, history sequence used to predict next N sequence.
        :param real_seq: tuple, correct sequence used to compare to prediction.
        :return: list of int, correct count of this sequence, with each point in time series separated.
        """
        result = [0] * self.pre_count
        try:
            predict_sequence = self.get_predict(his_seq)
            for i in range(self.pre_count):
                if real_seq[i] in predict_sequence[i]:
                    result[i] += 1
        except KeyError:
            pass
        return result

    def test_csv(self, file_dir: str):
        """
        Use all test data from a csv file to test markov model.

        :param file_dir: str, file directory of the csv file.
        :return: float, accuracy calculated using whole file's data.
        """
        aggregate = [0] * self.pre_count
        row_count = 0
        with open(file_dir, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                row_count += 1
                aggregate = [sum(x) for x in
                             zip(self.test_seq(tuple(row[-(self.his_count + self.test_count):-self.test_count]),
                                               tuple(row[-self.test_count:])), aggregate)]
        return [x/row_count for x in aggregate]

    def write_pre(self, test_dir: str, result_dir: str):
        """
        Predict sequences using test data and write predict result into a csv file.

        :param test_dir: str, test data's file directory
        :param result_dir: str, predict result's file directory
        """
        test_file = open(test_dir, 'r')
        result_file = open(result_dir, 'w', newline='')
        reader = csv.reader(test_file, delimiter=',')
        writer = csv.writer(result_file, delimiter=',')
        for row in reader:
            try:
                predict_sequence = self.get_predict(tuple(row[-(self.his_count + self.test_count):-self.test_count]))
                max_seq = []
                for point_list in predict_sequence:
                    if len(point_list) > 0:
                        max_seq.append(point_list[0])
                    else:
                        max_seq.append(None)
                writer.writerow(max_seq)
            except KeyError:
                writer.writerow([None] * self.pre_count)
        test_file.close()
        result_file.close()


if __name__ == '__main__':
    markov = Markov(his_count=1)
    markov.read_csv('trajectory100000.csv')
    print(markov.test_csv('trajectory100000.csv'))
    markov.write_pre('trajectory100000.csv', 'result.csv')
    print()
