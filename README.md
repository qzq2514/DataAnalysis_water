# DataAnalysis_water
小实习项目，帮助某公司进行水表和热力分析

项目使用python语言,主要使用numpy,pandas,matplotlib,scipy库等
项目分成分成多个模块,包括前期的排序、拟合、汇总、备注添加等。
该readme文件只是显示最后分析报告内,其他具体细节可以根据文件名找到。
#                                                       某小区用户用水量年报  
2016.10.31 - 2017.10.31
### 1.数据说明  
本次数据分析年报统计某小区211户家庭 共1718017条数据。具体统计时间从2016-10-31 15:59:00到2017-10-31 23:59:00  
### 2.统计结果  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/oneDay.PNG)  
从每天的用户用水量来看，居民主要用水时间段在晚上19:00到凌晨0:00之间，且该时间段的用水量占全天的用水量50%。居民的在凌晨1:00到凌晨5:00间用水量最少，仅占全天的10%。从上图来看，主要用水在晚上，居民进行做饭和洗浴需要使用大量的水。  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/oneWeek.PNG)  
从一周的居民用水量来看，居民用水在周日这天达到的一周用水量之最，且在周一到周三这三天仍然具有较高的用水量。而在周四，居民的用水量降低到一周最少。  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/oneWeek.PNG)  
根据一年的居民用水量分布情况来看，居民在6月到9月间的用水量为一年之最，该时间段为夏季炎热气候，居民洗浴，衣物的洗涤频繁可能是导致用水量高的原因。而一年中用水量在12月份达到的最低，该月用水量明显低于其他月份，甚至只有一年中最高用水量-7月的一半不到  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/oneQuarter.PNG)  
从上述的居民季度用水量来看，居民在第三季度的用水量达到的全年之最，其用水量占全年用水量的30%，第三季度对应于7月到9月，为夏季，这与上述按月统计的用水量的统计结果是一致的。其他季度的用水量从高到低分别为:第二季度，第一季度，第四季度，分别占全年用水量的28%,22%,20%。  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/hourInMonth.PNG)  
从上图每个月中24小时的用水量分布来看，在每个月内，晚上时间段内，即20:00-24:00这个时间段内，总是占有全天最大的比例，均占有40%左右的比重。而凌晨0:00-4:00和4:00-8:00之内的时间段占有最少的比重。  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/waterWithTemp2.PNG)  
从上述2017冬季(2月)的用水量和气温的关系图，我们可以大致看出用水量和气温还是呈现一种正相关的关系，在月初，当气温较低的时候，用水量也偏低，在月中下旬的时候，气温较高，用水量也达到了整个月的最高水平  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/waterWithTemp7.PNG)  
在2017.7夏季偏炎热气候时，用水量和气温都呈现一种较高的水平，且气温和用水量的变化趋势不明显，较为稳定。  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/top20.PNG)  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/hourInWeek.PNG)  
![](https://github.com/qzq2514/ImageForGithubMakdown/blob/master/DataAnalysis_water/tabla.PNG)  
根据上图标的分析，某些用户的全年的用水量不足10m2,甚至某些用户，像16104555，16104804用户出现了全年无用水，据此推断这些全年用水量极少的用户可能是空户，无人入住。
