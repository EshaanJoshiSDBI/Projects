library(unvotes)
library(ggplot2)
library(dplyr)
library(tidyr)
library(lubridate)
question1 = function()
{
  x = table(unlist(un_roll_call_issues$issue))
  x = as.data.frame.table(x)
  y = ggplot(x,aes(Var1,Freq)) + geom_bar(stat='identity', fill = 'blue', width = 0.5) + geom_text(aes(label = Freq),vjust = -0.3) + theme_minimal()
  z = ggplot(x,aes(Var1,Freq)) + geom_linerange(aes(Var1,ymin = 0, ymax = Freq), color = 'gray', size = 2) + geom_point(aes(color = Var1), size = 2) + ggpubr::color_palette('jco') + theme_bw()
  return (list(y,z))
}
question1()
question2 = function()
{
  y = un_roll_call_issues[order(un_roll_call_issues$rcid),]
  fir_occ = y[match(unique(y$issue), y$issue),]
  a = as.numeric(fir_occ[which(fir_occ$issue == 'Nuclear weapons and nuclear material'),1])
  q2_1_ = pull(un_roll_calls[which(un_roll_calls$rcid == a),][,4])
  q2_1 = paste('The date when the issue of Nuclear weapons and material was first discussed is',q2_1_)
  q2_2 = 'Yes the topic Nuclear weapons was discussed too late'
  return (list(q2_1, q2_2))
}
question2()
question3 = function()
{
  ans_ = un_votes %>% inner_join(un_roll_call_issues) %>% group_by(issue) %>% filter(vote == 'abstain') %>% summarize( votes = n())
  ans = ans_[which(ans_$votes == max(ans_$votes)),]
  votes_issues = un_votes %>% inner_join(un_roll_call_issues, by = 'rcid')
  ans_mean_ = votes_issues %>% group_by(issue) %>% summarize(percent_abstain = mean(vote == 'abstain')) %>% arrange(percent_abstain)
  ans_mean = ans_mean_[which(ans_mean_$percent_abstain == max(ans_mean_$percent_abstain)),]
  return (paste('The issue with most abstains is',ans[[1]],'with', ans[[2]],'abstain votes average of',ans_mean[[2]],'votes from all the abstain votes'))
}
question3()
question4 = function()
{
  ans_ = un_votes %>% group_by(country) %>% filter(vote == 'yes' | vote == 'no') %>% summarize(votes = n()) %>% arrange(desc(votes))
  ans = ans_[1,]
  return (paste('The country with most votes as yes or no is',ans[[1]],'with',ans[[2]],'clear stands'))
}
question4()
question5 = function()
{
  df = un_roll_calls[which(un_roll_calls$date > as.Date('2000-01-01')),]
  df1 = un_roll_call_issues %>% inner_join(df, by = 'rcid') %>% arrange(date) %>% select(-one_of('short_name','session','importantvote','unres','amend','para','short','descr'))
  df2 = df1 %>% group_by(issue) %>% summarize(times = n() , prop_isse = n()/nrow(df1))
  combined_proportion = df2[which(df2$issue == 'Human rights' | df2$issue == 'Economic development'),]
  combined_proportion_num = pull(combined_proportion[1,3] + combined_proportion[2,3])
  return (paste('The combined proportion of the two issues out of all the discussions is',combined_proportion_num,', so yes around one third of the debates are taken on these issues'))
}
question5()
question6 = function()
{
  df = un_roll_call_issues %>% inner_join(un_votes, by = 'rcid') %>% filter(country == 'India') %>% filter(issue == 'Human rights')
  ans = df %>% group_by(vote) %>% summarize(time = n(), prop = n()/nrow(df))
  return (paste('India abstained from voting in a Human Rights issue',ans[which(ans$vote == 'abstain'),][2],'times','proportion of',ans[which(ans$vote == 'abstain'),][3]))
}
question6()
question7 = function()
{
  # df_imp = un_roll_calls %>% inner_join(un_votes, by = 'rcid') %>% select(-one_of('session','date','unres','amend','para','short','descr','country_code')) %>% filter()
  df1 = un_roll_calls %>% inner_join(un_votes, by = 'rcid') %>%select(-one_of('session','date','unres','amend','para','short','descr','country_code')) %>% filter(country == 'India') %>% filter(importantvote == 1)
  df1_1 = df1 %>% group_by(vote) %>% summarize(times = n(), proportion = n()/nrow(df1))
  ans1 = df1_1[which(df1_1$vote == 'abstain'),]
  ans1_state = paste('India abstain from voting',ans1[1,2],'times on important voting, proportion being',ans1[1,3])
  df2 = un_roll_calls %>% inner_join(un_votes, by = 'rcid') %>% select(-one_of('session','date','unres','amend','para','short','descr','country_code')) %>% filter(country == 'India')
  df2_1 = subset(df2,df2$importantvote == 1 | is.na(df2$importantvote))
  df2_2 =  df2_1 %>% group_by(vote) %>% summarize(times = n(), proportion = n()/nrow(df2_1))
  ans2_ = df2_2[which(df2_2$vote == 'abstain'),]
  ans2_state = paste('When we include the votes where the importance isn\'t specified then the count increases to', ans2_[1,2],'proportion decreases to',ans2_[1,3])
  df3 = un_roll_calls %>% inner_join(un_votes, by = 'rcid') %>% select(-one_of('session','date','unres','amend','para','short','descr','country_code')) %>% filter(country == 'United States') %>% filter(importantvote == 1) #%>% filter(vote == 'abstain')
  df3_1 = df3 %>% filter(vote == 'abstain') %>% group_by(country) %>% summarise(votes = n(), prop = votes/ nrow(df3))
  #ans3_India = df3_1[which(df3_1$country == 'India'),]
  ans3_India = ans1[1,3]
  ans3_usa = df3_1[which(df3_1$country == 'United States'),]
  absent = un_votes %>% inner_join(un_roll_calls, by = 'rcid') %>% select(-one_of('session','date','unres','amend','para','short','descr','country_code')) %>% filter(importantvote == 1)
  India_absent = n_distinct(absent$rcid) - (absent %>% filter(country == 'India') %>% nrow()) 
  prop_India_absent = India_absent / n_distinct(absent$rcid)
  usa_absent = n_distinct(absent$rcid) - (absent %>% filter(country == 'United States') %>% nrow())
  prop_usa_absent = usa_absent / n_distinct(absent$rcid)
  ans3_ = (ans3_India + prop_India_absent)/(ans3_usa[1,3] + prop_usa_absent)
  ans3_state = paste('The proportion of proportion of abstain of India and US is',ans3_,'i.e Indias proportion of abstain is more than USs proportion of abstain')
  return(c('Ans1:',ans1_state,'Ans2:',ans2_state,'Ans3:',ans3_state))
}
question7()
question8 = function()
{
  df_India = un_votes %>% inner_join(un_roll_calls, by = 'rcid') %>% select(-one_of('session','unres','amend','para','short','descr','country_code')) %>% filter(country == 'India')
  df_Usa = un_votes %>% inner_join(un_roll_calls, by = 'rcid') %>% select(-one_of('session','unres','amend','para','short','descr','country_code')) %>% filter(country == 'United States')
  df = merge(df_India, df_Usa, by = 'rcid')
  before = subset(df, df$date.x < as.Date('2001-01-01'))
  after = subset(df, df$date.x >= as.Date('2001-01-01'))
  compare = length(which(df$vote.x == df$vote.y))
  compare_prop = compare / nrow(df)
  ans1_state = paste('The proportion of voting when India has casted the same vote as US is', compare_prop)
  compare_before = length(which(before$vote.x == before$vote.y))
  compare_before_prop = compare_before / nrow(before)
  compare_after = length(which(after$vote.x == after$vote.y))
  compare_after_prop = compare_after / nrow(after)
  ans2_state = paste('The proportion before is',compare_before_prop,'and the proportion after 2001 is',compare_after_prop,'the claim India blindly follows US is false')
  return (c(ans1_state,ans2_state))
}
question8()
question9 = function()
{
  df_India = un_votes %>% inner_join(un_roll_calls, by = 'rcid')  %>% filter(country == 'India')
  df_Usa = un_votes %>% inner_join(un_roll_calls, by = 'rcid')  %>% filter(country == 'United States')
  df_Russia = un_votes %>% inner_join(un_roll_calls, by = 'rcid') %>% filter(country == 'Russia')
  #df_India_Russia = merge(df_India, df_Russia, by = 'rcid')
  #df_India_usa = merge(df_India,df_Usa, by = 'rcid')
  #df_Russia_usa = merge(df_Russia, df_Usa, by = 'rcid')
  #df_Russia_usa_before = df_Russia_usa[which(df_Russia_usa$vote.x == df_Russia_usa$vote.y & df_Russia_usa$date.x < as.Date('2001-01-01')),]
  #df_Russia_usa_after = df_Russia_usa[which(df_Russia_usa$vote.x == df_Russia_usa$vote.y & df_Russia_usa$date.x >= as.Date('2001-01-01')),]
  Russia_USA = inner_join(df_Russia, df_Usa, by = "rcid" )
  India_Russia_USA = inner_join(df_India, Russia_USA, by = "rcid" )
  IRU = India_Russia_USA[,c(1,2,4,7,13,15,18,24,26,29)]
  Russia_USA_Votes= which(IRU$vote.x!=IRU$vote.y)
  Russia_USA_before= which( IRU$vote.x!=IRU$vote.y & IRU$date< "2001/01/01")
  Russia_USA_after= which( IRU$vote.x!=IRU$vote.y & IRU$date>= "2001/01/01")
  India_Russia_before = which(IRU$vote.x!=IRU$vote.y & IRU$vote== IRU$vote.x & IRU$date< "2001/01/01" )
  Prop_India_Russia_before= length(India_Russia_before)/length(Russia_USA_before)
  India_USA_before = which(IRU$vote.x!=IRU$vote.y & IRU$vote== IRU$vote.y & IRU$date<="2001/01/01" )
  Prop_India_USA_before= length(India_USA_before)/length(Russia_USA_before)
  India_Russia_after = which(IRU$vote.x!=IRU$vote.y & IRU$vote== IRU$vote.x & IRU$date>="2001/01/01" )
  IRU_after=subset(IRU, IRU$date >="2001/01/01" )
  Prop_India_Russia_after= length(India_Russia_after)/length(Russia_USA_after)
  India_USA_after = which(IRU$vote.x!=IRU$vote.y & IRU$vote== IRU$vote.y & IRU$date>="2001/01/01" )
  Prop_India_USA_after= length(India_USA_after)/length(Russia_USA_after)
  return(paste('Proportion of India and Russia before 2001:',Prop_India_Russia_before,'proportion of India and USA before 2001',Prop_India_USA_before,'proportion of India and Russia after 2001',Prop_India_Russia_after,'proportion of India and USA after 2001',Prop_India_USA_after))
}
question9()
question10 = function()
{
  df2 = un_votes %>% inner_join(un_roll_calls, by = 'rcid')
  df3 = df2 %>% group_by(country, year = year(date)) %>% summarize(votes = n(), pct_yes = mean(vote == 'yes'))
  plot_ = df3 %>% filter(country == 'India') %>% ggplot(aes(x=year, y = pct_yes)) + geom_point() + geom_line()
  return(plot_)
}
question10()
# Answers
#Q1)
question1()
#Q2)
question2()
#Q3)
question3()
#Q4)
question4()
#Q5)
question5()
#Q6)
question6()
#Q7)
question7()
#Q8)
question8()
#Q9)
question9()
#Q10)
question10()
