'''
Created on 2018年4月19日

@author:YHJ
'''
import numpy as np
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
class Feature_Analyse(FeatureCalculater):
    def load_data_set(self):
        sql="select * from Analyse_int"
        self.executer.execute(sql)
        result=self.executer.fetchall()
        data_set=np.array(result)
        print(data_set)
        return data_set


    def create_C1(self,data_set):
        """
        Create frequent candidate 1-itemset C1 by scaning data set.
        Args:
            data_set: A list of transactions. Each transaction contains several items.
        Returns:
            C1: A set which contains all frequent candidate 1-itemsets
        """
        C1 = set()
        for t in data_set:
            for item in t:
                item_set = frozenset([item])
                C1.add(item_set)
        return C1
    
    
    def is_apriori(self,Ck_item, Lksub1):
        """
        Judge whether a frequent candidate k-itemset satisfy Apriori property.
        Args:
            Ck_item: a frequent candidate k-itemset in Ck which contains all frequent
                     candidate k-itemsets.
            Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
        Returns:
            True: satisfying Apriori property.
            False: Not satisfying Apriori property.
        """
        for item in Ck_item:
            sub_Ck = Ck_item - frozenset([item])
            if sub_Ck not in Lksub1:
                return False
        return True
    
    
    def create_Ck(self,Lksub1, k):
        """
        Create Ck, a set which contains all all frequent candidate k-itemsets
        by Lk-1's own connection operation.
        Args:
            Lksub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets.
            k: the item number of a frequent itemset.
        Return:
            Ck: a set which contains all all frequent candidate k-itemsets.
        """
        Ck = set()
        len_Lksub1 = len(Lksub1)
        list_Lksub1 = list(Lksub1)
        for i in range(len_Lksub1):
            for j in range(1, len_Lksub1):
                l1 = list(list_Lksub1[i])
                l2 = list(list_Lksub1[j])
                l1.sort()
                l2.sort()
                if l1[0:k-2] == l2[0:k-2]:
                    Ck_item = list_Lksub1[i] | list_Lksub1[j]
                    # pruning
                    if self.is_apriori(Ck_item, Lksub1):
                        Ck.add(Ck_item)
        return Ck
    
    
    def generate_Lk_by_Ck(self,data_set, Ck, min_support, support_data):
        """
        Generate Lk by executing a delete policy from Ck.
        Args:
            data_set: A list of transactions. Each transaction contains several items.
            Ck: A set which contains all all frequent candidate k-itemsets.
            min_support: The minimum support.
            support_data: A dictionary. The key is frequent itemset and the value is support.
        Returns:
            Lk: A set which contains all all frequent k-itemsets.
        """
        Lk = set()
        item_count = {}
        for t in data_set:
            for item in Ck:
                if item.issubset(t):
                    if item not in item_count:
                        item_count[item] = 1
                    else:
                        item_count[item] += 1
        t_num = float(len(data_set))
        for item in item_count:
            if (item_count[item] / t_num) >= min_support:
                Lk.add(item)
                support_data[item] = item_count[item] / t_num
        return Lk
    
    
    def generate_L(self,data_set, k, min_support):
        """
        Generate all frequent itemsets.
        Args:
            data_set: A list of transactions. Each transaction contains several items.
            k: Maximum number of items for all frequent itemsets.
            min_support: The minimum support.
        Returns:
            L: The list of Lk.
            support_data: A dictionary. The key is frequent itemset and the value is support.
        """
        support_data = {}
        C1 = self.create_C1(data_set)
        L1 = self.generate_Lk_by_Ck(data_set, C1, min_support, support_data)
        Lksub1 = L1.copy()
        L = []
        L.append(Lksub1)
        for i in range(2, k+1):
            Ci = self.create_Ck(Lksub1, i)
            Li = self.generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
            Lksub1 = Li.copy()
            L.append(Lksub1)
        # for l in L:
        #     print(l)
        # print(support_data)
        return L, support_data
    
    
    def generate_big_rules(self,L, support_data, min_conf):
        """
        Generate big rules from frequent itemsets.
        Args:
            L: The list of Lk.
            support_data: A dictionary. The key is frequent itemset and the value is support.
            min_conf: Minimal confidence.
        Returns:
            big_rule_list: A list which contains all big rules. Each big rule is represented
                           as a 3-tuple.
        """
        big_rule_list = []
        sub_set_list = []
        for i in range(0, len(L)):
            for freq_set in L[i]:
                for sub_set in sub_set_list:
                    if sub_set.issubset(freq_set):
                        conf = support_data[freq_set] / support_data[freq_set - sub_set]
                        big_rule = (freq_set - sub_set, sub_set, conf)
                        if conf >= min_conf and big_rule not in big_rule_list:
                            # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                            big_rule_list.append(big_rule)
                sub_set_list.append(freq_set)
        return big_rule_list


if __name__ == "__main__":
    """
    Test
    """
    fa=Feature_Analyse()
    data_set = fa.load_data_set()
    L, support_data = fa.generate_L(data_set, k=3, min_support=0.2)
    big_rules_list = fa.generate_big_rules(L, support_data, min_conf=0.7)
    for item in big_rules_list:
        # conf 表示可信度
        print("freq_set-sub_set:%s => , sub_set:%s, conf: %s " %(item[0],item[1],item[2]))
    print("程序结束")