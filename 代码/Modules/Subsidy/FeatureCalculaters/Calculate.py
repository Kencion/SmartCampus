import Student
from Tools import MyDataBase
from tqdm import tqdm
from card import AvgDaysCostsCalculater
from card import BalanceRankCalculater
from card import CardDaysCalculater
from card import CardRechargeCalculater
from card import ConsumeTimes11_12Calculater
from dorm import CostAmountCalculater
from dorm import CostAverageDayDinnerHallCalculater
from dorm import CostAverageDayLaundryRoomCalculater
from dorm import CostAverageDaySupermarketCalculater
from dorm import CostTimesDayDinnerHallCalculater
from dorm import CostTimesDayLaundryRoomCalculater
from dorm import CostTimesDaySupermarketCalculater
from dorm import CostRateDinnerHallCalculater
from dorm import CostRateLaundryRoomCalculater
from dorm import CostRateSupermarketCalculater
from dorm import CostVarianceCalculater
from dorm import CosumeTimes0_25Calculater
from dorm import CountCost0_10Calculater
from library import LibraryBorrowCalculater
from library import LibraryTimesCalculater
from library import LibraryTimeSpandCalculater
from card import MaxCost7_8Calculater
from score import ScoreRankCalculater
import SubsidyCalculater
from card import Time6_7CostsCalculater
from card import Time7_8CostsCalculater
from card import TotalDinnerCostsCalculater
from card import Avg_ChargeCaculater
from card import Below2_5_RankCalculater
from card import Below10_RankCalculater
from score import Num_Of_1000Calculater
from score import Num_Of_2000Calculater
from score import Num_Of_1500Calculater
from score import PropotionCalculater1000
from score import PropotionCalculater2000
from score import PropotionCalculater1500
from score import scorerank_divided_by_stunum
from score import Stu_Num_Calculater
from card import Time7_8Consume_Avg


Student = Student.Student
AvgDaysCostsCalculater = AvgDaysCostsCalculater()          
Below10_RankCalculater=Below10_RankCalculater()       
BalanceRankCalculater = BalanceRankCalculater()                  
CardDaysCalculater = CardDaysCalculater()               
CardRechargeCalculater = CardRechargeCalculater()                   
ConsumeTimes11_12Calculater = ConsumeTimes11_12Calculater()                      
CostAmountCalculater = CostAmountCalculater()                 
CostAverageDayDinnerHallCalculater = CostAverageDayDinnerHallCalculater()                
CostAverageDayLaundryRoomCalculater = CostAverageDayLaundryRoomCalculater()              
CostAverageDaySupermarketCalculater = CostAverageDaySupermarketCalculater()                     
CostTimesDayDinnerHallCalculater = CostTimesDayDinnerHallCalculater()                    
CostTimesDayLaundryRoomCalculater = CostTimesDayLaundryRoomCalculater()                  
CostTimesDaySupermarketCalculater = CostTimesDaySupermarketCalculater()                       
CostRateDinnerHallCalculater = CostRateDinnerHallCalculater()                    
CostRateLaundryRoomCalculater = CostRateLaundryRoomCalculater()                  
CostRateSupermarketCalculater = CostRateSupermarketCalculater()    
CostVarianceCalculater = CostVarianceCalculater()                 
CosumeTimes0_25Calculater = CosumeTimes0_25Calculater()                    
CountCost0_10Calculater = CountCost0_10Calculater()                    
LibraryBorrowCalculater = LibraryBorrowCalculater()                    
LibraryTimesCalculater = LibraryTimesCalculater()                   
LibraryTimeSpandCalculater = LibraryTimeSpandCalculater()                       
MaxCost7_8Calculater = MaxCost7_8Calculater()                 
ScoreRankCalculater = ScoreRankCalculater()              
SubsidyCalculater = SubsidyCalculater()           
Time6_7CostsCalculater = Time6_7CostsCalculater()                 
Time7_8CostsCalculater = Time7_8CostsCalculater()                 
TotalDinnerCostsCalculater = TotalDinnerCostsCalculater()                      
Avg_ChargeCaculater = Avg_ChargeCaculater()                      
Below2_5_RankCalculater = Below2_5_RankCalculater()                       
Num_Of_1000Calculater = Num_Of_1000Calculater()                       
Num_Of_2000Calculater = Num_Of_2000Calculater()                       
Num_Of_1500Calculater = Num_Of_1500Calculater()                       
PropotionCalculater1000 = PropotionCalculater1000()                       
PropotionCalculater2000 = PropotionCalculater2000()                       
PropotionCalculater1500 = PropotionCalculater1500()                       
scorerank_divided_by_stunum = scorerank_divided_by_stunum()                       
Stu_Num_Calculater = Stu_Num_Calculater()
Time7_8Consume_Avg = Time7_8Consume_Avg()

calculater = [
#             Stu_Num_Calculater,
#             Num_Of_1000Calculater,
#             Num_Of_2000Calculater,
#             Num_Of_1500Calculater,

            ScoreRankCalculater,
            Below10_RankCalculater,
            Time6_7CostsCalculater,
            Time7_8CostsCalculater,
            TotalDinnerCostsCalculater,
            AvgDaysCostsCalculater,
            BalanceRankCalculater,
            CardDaysCalculater,
            CardRechargeCalculater,
            ConsumeTimes11_12Calculater,
            CostAmountCalculater,
            CostAverageDayDinnerHallCalculater,
            CostAverageDayLaundryRoomCalculater,
            CostAverageDaySupermarketCalculater,
   
            CostRateDinnerHallCalculater,
            CostRateLaundryRoomCalculater,
            CostRateSupermarketCalculater,
               
            CostTimesDayDinnerHallCalculater,
            CostTimesDayLaundryRoomCalculater,
            CostTimesDaySupermarketCalculater,
            CostVarianceCalculater,
            CosumeTimes0_25Calculater,
            CountCost0_10Calculater,
            LibraryBorrowCalculater,
            LibraryTimesCalculater,
            LibraryTimeSpandCalculater,
            MaxCost7_8Calculater,
            Avg_ChargeCaculater,
            Below2_5_RankCalculater,
                           
            PropotionCalculater1000,
            PropotionCalculater2000,
             PropotionCalculater1500,
            scorerank_divided_by_stunum,
            SubsidyCalculater,
            Time7_8Consume_Avg
            ]

# calculater = [SubsidyCalculater]

def calculate():
    db = MyDataBase.MyDataBase("train")
    conn = db.getConn()
    executer = db.getExcuter()

    
    sql = "select student_id from score"
    executer.execute(sql)
    studentIds = executer.fetchall()
    db.close()
     
#     for i in tqdm(studentIds):
#         i = i[0]
#         student = Student(studentId=i)
#         student.calculate(calculater)
           
    for i in calculater:
        i.setLevel()
      
    for i in tqdm(studentIds):
        i = i[0]
        student = Student(studentId=i)
        student.rankit(calculater)
     
    for i in calculater:
        i.afterCalculate()

if __name__ == '__main__':
    calculate()
